"""Where things live: the repository root, its .frontdoor folder, the board and the daemon state."""

from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
CORE = SCRIPTS.parent
ASSETS = CORE / "assets"


def repo_root(start=None):
    """The nearest folder holding .git, walking up from start (default: the current folder); start itself when none does."""
    here = Path(start or Path.cwd()).resolve()
    for folder in (here, *here.parents):
        if (folder / ".git").exists():
            return folder
    return here


def frontdoor_dir(root):
    return Path(root) / ".frontdoor"


def board_dir(root):
    return frontdoor_dir(root) / "board"


def daemon_state(root):
    return frontdoor_dir(root) / "fd-daemon.json"


def daemon_log(root):
    return frontdoor_dir(root) / "fd-daemon.log"


def ensure_ignored(root):
    """Add .frontdoor/ to the repository's .gitignore when it is a repository and the entry is missing. Returns a message or None."""
    root = Path(root)
    if not ((root / ".git").exists() or (root / ".gitignore").exists()):
        return None
    ignore = root / ".gitignore"
    text = ignore.read_text(encoding="utf-8") if ignore.exists() else ""
    if any(line.strip().strip("/") == ".frontdoor" for line in text.splitlines()):
        return None
    prefix = "" if not text or text.endswith("\n") else "\n"
    with ignore.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{prefix}.frontdoor/\n")
    return f"added .frontdoor/ to {ignore}"
