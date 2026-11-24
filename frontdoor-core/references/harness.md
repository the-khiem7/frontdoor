# The harness `fd`

One command for the repeated work of the frontdoor skills, so an agent runs a line instead of writing the step out. Run it from inside the repository being worked on; `--repo <dir>` names the repository root instead (default: the nearest folder with `.git`).

| Needs | Run as |
|---|---|
| nothing but Python (`page`, `round`, `choose`, `status`, `board`, `contrast`) | `uvx python -I <frontdoor-core>/scripts/fd.py <command>` |
| a browser and Pillow (`render`, `animate`, `daemon`) | `uvx --from playwright --with pillow python -I <frontdoor-core>/scripts/fd.py <command>` |

The browser is the Edge or Chrome already on the machine; nothing is downloaded and no administrator rights are needed. Every command prints what it changed and where; errors are one line on stderr starting with `fd:`. Exit 0 is success, 1 a failure or a render WARN, 2 a wrong argument.

## Board

| Command | Does |
|---|---|
| `fd page add <slug> [--title T]` | adds a page; `fd page list` lists them |
| `fd round new <slug> --count N [--title T] [--note T] [--seed FILE]` | starts the page's next round: a folder per variant and `round.json`; `--count` is required |
| `fd round add <slug> [<n>]` | publishes the round (default: the latest draft) from `round.json` and the renders; again after a change |
| `fd choose <slug> <n> <ids> [--note T] [--variant-note ID=T]` | records the choice, several ids for a mix, with a note on the round and on each variant |
| `fd choose --from <file or ->` | records the text the board's Copy choice button gave, read from its last `fd-choice` line; a choice with no variant records that every variant was rejected |
| `fd status [<slug>] [--json]` | one line per page, and whether the daemon runs |
| `fd board build` / `fd board open` | rebuilds the page after a hand edit of `board.json` / opens it |

How a round is run is in `board.md`.

## Pictures

| Command | Does |
|---|---|
| `fd render <page.html> --out <dir> [--root <dir>] [--items a,b] [--themes light,dark] [--max-kb 300] [--method 4] [--watch]` | renders every `.item` to `<id>.webp` and `<id>-dark.webp` (a `data-social` item to PNG) and prints each file, the fonts and the grounds; the contract is in `source-page.md` |
| `fd render ... --watch` | renders again whenever a file under the served root changes (HTML, CSS, JS, SVG, JSON, fonts), keeping the browser open; Ctrl-C stops |
| `fd animate <page.html> --item <id> --call "draw({v})" --out <dir> [...]` | a looping animated WebP of one item; every option is that of `scripts/animate.py`, whose docstring explains the motions, `--draft` and `--batch` |
| `fd contrast <fg> <bg> [...]` | the WCAG ratio of each colour pair; exit 1 under 4.5 |

`--root` is the folder served over HTTP: it must hold the page and everything it links to. `--method` is libwebp's effort; the output is lossless, so every method gives the same pixels, and 4 is the default because it costs about half the time of 6 for files 0.06 percent smaller in total on 20 pictures.

## Daemon

`fd daemon start` starts a background process that keeps one browser and one encoder pool open, so every later `fd render` in the repository skips the browser start. Start it at the beginning of design work that renders more than a few times. It listens on 127.0.0.1 only, answers only callers holding the token in `.frontdoor/fd-daemon.json`, logs to `.frontdoor/fd-daemon.log`, and stops after 30 idle minutes (`--idle <seconds>`). `fd daemon status` and `fd daemon stop` do what they say. `fd render` uses the daemon when it answers and renders in its own process otherwise; `--no-daemon` forces the second. `fd animate` always runs in its own process.
