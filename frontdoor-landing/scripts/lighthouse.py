#!/usr/bin/env python
"""Run Lighthouse against a static page folder and print the four scores plus the audits that lost points.

    uvx python -I lighthouse.py <root> [--page index.html] [--preset mobile|desktop] [--out report.json]

It serves <root> over HTTP, starts the machine's Edge or Chrome headless with a remote debugging
port, and points `npx lighthouse` at that port. Starting the browser yourself matters: on Windows,
Lighthouse's own launch of Edge fails with "waiting for dynamic debugging port". `npx` downloads
Lighthouse into the user's cache, no admin rights needed. Needs Node.

Performance scores swing by 10 points or more between identical runs, especially while other work
is using the machine; run it twice and report the range, not one number.
"""
import argparse
import functools
import http.server
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


class QuietServer(http.server.ThreadingHTTPServer):
    def handle_error(self, request, client_address):
        pass  # a browser closing a connection early is not an error here


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def find_browser():
    for path in BROWSERS:
        if Path(path).is_file():
            return path
    for name in ("microsoft-edge", "google-chrome", "chromium", "chromium-browser", "msedge", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("lighthouse.py: no Edge or Chrome found.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--page", default="index.html")
    ap.add_argument("--preset", default="mobile", choices=["mobile", "desktop"])
    ap.add_argument("--out")
    a = ap.parse_args()

    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        sys.exit("lighthouse.py: npx not found; install Node.js.")

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = QuietServer(
        ("127.0.0.1", 0), functools.partial(Quiet, directory=str(Path(a.root).resolve())))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_address[1]}/{a.page}"

    profile = tempfile.mkdtemp(prefix="lh-profile-")
    port = free_port()
    browser = subprocess.Popen(
        [find_browser(), "--headless=new", f"--remote-debugging-port={port}", f"--user-data-dir={profile}",
         "--no-first-run", "--disable-extensions", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    report = Path(a.out) if a.out else Path(tempfile.gettempdir()) / "lighthouse-report.json"
    try:
        for _ in range(50):
            with socket.socket() as s:
                if s.connect_ex(("127.0.0.1", port)) == 0:
                    break
            time.sleep(0.2)
        else:
            sys.exit("lighthouse.py: the browser did not open its debugging port.")
        cmd = [npx, "--yes", "lighthouse", url, "--port", str(port), "--quiet",
               "--only-categories=performance,accessibility,best-practices,seo",
               "--output=json", f"--output-path={report}"]
        if a.preset == "desktop":
            cmd.append("--preset=desktop")
        run = subprocess.run(cmd, capture_output=True, text=True, shell=(os.name == "nt"))
        if run.returncode != 0 or not report.is_file():
            sys.exit(f"lighthouse.py: lighthouse failed.\n{run.stderr[-1500:]}")
    finally:
        browser.terminate()
        try:
            browser.wait(timeout=10)
        except subprocess.TimeoutExpired:
            browser.kill()
        shutil.rmtree(profile, ignore_errors=True)
        server.shutdown()

    data = json.loads(report.read_text(encoding="utf-8"))
    print(f"preset {a.preset}, {url}")
    for key, cat in data["categories"].items():
        print(f"  {cat['title']}: {round(cat['score'] * 100)}")
    lost = [(c["id"], data["audits"][c["id"]]) for cat in data["categories"].values() for c in cat["auditRefs"]
            if data["audits"][c["id"]].get("score") is not None and data["audits"][c["id"]]["score"] < 0.9
            and c.get("weight", 0) > 0]
    seen = set()
    for audit_id, audit in lost:
        if audit_id in seen:
            continue
        seen.add(audit_id)
        print(f"  lost points: {audit['title']} (score {audit['score']})")
    print(f"report: {report}")


if __name__ == "__main__":
    main()
