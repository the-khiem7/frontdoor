"""Tests of the frontdoor harness (frontdoor-core/scripts). Not shipped with any skill.

    uvx --with pytest --with pillow --with playwright pytest tests                   # everything that needs no browser
    uvx --with pytest --with pillow --with playwright pytest tests --browser-tests   # also drive the installed Edge or Chrome
"""

import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "frontdoor-core" / "scripts"
sys.path.insert(0, str(SCRIPTS))


def pytest_addoption(parser):
    parser.addoption("--browser-tests", action="store_true", help="run the tests that launch the installed Edge or Chrome")


def pytest_configure(config):
    config.addinivalue_line("markers", "browser: launches the installed Edge or Chrome; run with --browser-tests")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--browser-tests"):
        return
    skip = pytest.mark.skip(reason="needs --browser-tests")
    for item in items:
        if "browser" in item.keywords:
            item.add_marker(skip)


@pytest.fixture
def repo(tmp_path):
    """An empty repository: a folder with .git, as fd finds the root by it."""
    (tmp_path / ".git").mkdir()
    return tmp_path


@pytest.fixture
def fd(repo, capsys):
    """Run one fd command against the test repository; returns (exit code, stdout, stderr)."""
    from fdlib.cli import main

    def run(*args):
        code = main(["--repo", str(repo), *map(str, args)])
        out = capsys.readouterr()
        return code, out.out, out.err

    return run


@pytest.fixture
def board(repo):
    """Read the board record as fd left it."""
    def read():
        return json.loads((repo / ".frontdoor" / "board" / "board.json").read_text(encoding="utf-8"))

    return read
