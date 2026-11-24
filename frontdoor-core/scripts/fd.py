#!/usr/bin/env python
"""fd, the frontdoor harness: the design board, the renderer and its browser daemon.

    uvx --from playwright --with pillow python -I fd.py <command> ...     (render, animate, daemon)
    uvx python -I fd.py <command> ...                                     (page, round, choose, status, board, contrast)

Run `fd.py --help` for the commands; references/harness.md describes each one.
"""

import sys
from pathlib import Path

# -I leaves the script's own folder off sys.path, so the package beside this file is added by hand.
sys.path.insert(0, str(Path(__file__).resolve().parent))

if __name__ == "__main__":
    from fdlib.cli import main

    sys.exit(main())
