"""A background process that keeps one browser and one encoder pool open, so each `fd render` skips the browser start.

It listens on 127.0.0.1 only, on a free port, and answers only requests that carry the token it wrote to
<repo>/.frontdoor/fd-daemon.json (ignored by git). Jobs run one at a time on the thread that owns the browser, because
Playwright's sync API is bound to one thread. It stops itself after --idle seconds without a job (default 30 minutes).
"""

import http.server
import json
import os
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from . import FdError
from .paths import daemon_log, daemon_state, frontdoor_dir

IDLE_DEFAULT = 1800


def read_state(root):
    path = daemon_state(root)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def call(state, path, payload=None, timeout=5.0):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(f"http://127.0.0.1:{state['port']}{path}", data=data, method="POST" if data is not None else "GET",
                                 headers={"X-FD-Token": state["token"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def alive(root):
    """The daemon's state when it answers, else None (and a stale state file is removed)."""
    state = read_state(root)
    if not state:
        return None
    try:
        info = call(state, "/status", timeout=1.0)
        return {**state, **info}
    except (OSError, urllib.error.URLError, ValueError):
        try:
            daemon_state(root).unlink()
        except OSError:
            pass
        return None


def run(root, idle=IDLE_DEFAULT, browser=None, workers=None):
    """Serve render jobs in the foreground until stopped or idle."""
    from .render import Renderer

    root = Path(root)
    frontdoor_dir(root).mkdir(parents=True, exist_ok=True)
    token = secrets.token_hex(16)
    renderer = Renderer(browser=browser, workers=workers, keep_pool=True).start()
    started = time.time()
    state = {"last": time.time(), "stop": False, "jobs": 0}

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def _reply(self, code, body):
            data = json.dumps(body).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _authorised(self):
            if not secrets.compare_digest(self.headers.get("X-FD-Token", ""), token):
                self._reply(403, {"error": "bad token"})
                return False
            return True

        def do_GET(self):
            if not self._authorised():
                return
            if self.path == "/status":
                self._reply(200, {"pid": os.getpid(), "jobs": state["jobs"], "uptime": round(time.time() - started),
                                  "idle_left": round(idle - (time.time() - state["last"]))})
            else:
                self._reply(404, {"error": "unknown path"})

        def do_POST(self):
            if not self._authorised():
                return
            length = int(self.headers.get("Content-Length") or 0)
            try:
                body = json.loads(self.rfile.read(length) or b"{}")
            except ValueError:
                self._reply(400, {"error": "bad JSON"})
                return
            if self.path == "/stop":
                state["stop"] = True
                self._reply(200, {"stopped": True})
            elif self.path == "/render":
                lines = []
                try:
                    problems = renderer.render(body, lines.append)
                except (ValueError, RuntimeError) as e:
                    problems, lines = -1, lines + [f"fd: {e}"]
                except Exception as e:  # noqa: BLE001 - the browser died: start a fresh one for the next job
                    problems, lines = -1, lines + [f"fd: render failed in the daemon ({e}); the browser is restarted."]
                    renderer.browser = None
                state["jobs"] += 1
                state["last"] = time.time()
                self._reply(200, {"problems": problems, "lines": lines})
            else:
                self._reply(404, {"error": "unknown path"})

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    server.timeout = 2.0
    tmp = daemon_state(root).with_name("fd-daemon.json.tmp")
    tmp.write_text(json.dumps({"pid": os.getpid(), "port": server.server_address[1], "token": token, "started": started}), encoding="utf-8")
    tmp.replace(daemon_state(root))
    print(f"fd daemon: listening on 127.0.0.1:{server.server_address[1]}, pid {os.getpid()}, idle stop after {idle} s", flush=True)
    try:
        while not state["stop"] and time.time() - state["last"] < idle:
            server.handle_request()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        renderer.close()
        current = read_state(root)
        if current and current.get("token") == token:
            try:
                daemon_state(root).unlink()
            except OSError:
                pass
        print("fd daemon: stopped", flush=True)


def start(root, script, idle=IDLE_DEFAULT, browser=None, wait=30.0):
    """Start the daemon as a detached process and wait until it answers."""
    running = alive(root)
    if running:
        return running, False
    frontdoor_dir(root).mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-I", str(script), "--repo", str(root), "daemon", "run", "--idle", str(idle)]
    if browser:
        cmd += ["--browser", browser]
    kwargs = {"stdin": subprocess.DEVNULL, "stderr": subprocess.STDOUT, "close_fds": True}
    with open(daemon_log(root), "a", encoding="utf-8") as log:  # the child keeps its own handle
        if sys.platform.startswith("win"):
            flags = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            try:
                # Leave the job object of the calling shell, so the daemon outlives the command that started it.
                proc = subprocess.Popen(cmd, stdout=log, creationflags=flags | subprocess.CREATE_BREAKAWAY_FROM_JOB, **kwargs)
            except OSError:
                proc = subprocess.Popen(cmd, stdout=log, creationflags=flags, **kwargs)
        else:
            proc = subprocess.Popen(cmd, stdout=log, start_new_session=True, **kwargs)
    deadline = time.time() + wait
    while time.time() < deadline:
        if proc.poll() is not None:
            raise FdError(f"the daemon exited at start (code {proc.returncode}); see {daemon_log(root)}.")
        running = alive(root)
        if running:
            return running, True
        time.sleep(0.2)
    raise FdError(f"the daemon did not answer within {wait:.0f} s; see {daemon_log(root)}.")


def stop(root):
    state = alive(root)
    if not state:
        return False
    try:
        call(state, "/stop", {}, timeout=5.0)
    except (OSError, urllib.error.URLError):
        pass
    for _ in range(50):
        if not daemon_state(root).exists():
            break
        time.sleep(0.1)
    return True


def render(state, job, timeout=600.0):
    return call(state, "/render", job, timeout=timeout)
