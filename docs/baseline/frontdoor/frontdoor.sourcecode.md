---
baseline_schema: "2.0"
pack: "frontdoor"
document: "sourcecode"
status: "active"
updated: "2026-11-24"
code_ref: "uncommitted"
---

# Frontdoor: Topology and Execution Flow

## Folders

```text
frontdoor-readme/
  SKILL.md
  agents/      openai.yaml
  scripts/     animate.py  board.py
  references/  github-readme.md  audit-and-plan.md  readme-content.md  banner.md  signature.md
frontdoor-illustrate/
  SKILL.md
  agents/      openai.yaml
  scripts/     render.py  contrast.py  board.py
  assets/      starter.css  starter.html  shared.js
  references/  source-page.md  scene-craft.md  signature.md
frontdoor-landing/
  SKILL.md
  agents/      openai.yaml
  scripts/     shoot.py  lighthouse.py  board.py
  references/  existing-landing.md  pages-setup.md  page-craft.md  motion.md  verify.md  signature.md
frontdoor-ui-gallery/
  SKILL.md
  agents/      openai.yaml
  scripts/     shoot.py  real.ps1
  assets/      gallery.html  mock-kit.ts  fixtures.ts  vite.gallery.ts
  references/  states.md  manifest.md  real-capture.md  stacks/ (index.md  wails3.md  tauri2.md  svelte.md  vue.md)
frontdoor-core/
  SKILL.md
  agents/      openai.yaml
  scripts/     fd.py  fdlib/ (cli.py  board.py  render.py  daemon.py  paths.py)  animate.py  contrast.py
  assets/      board.html  starter.css  starter.html  shared.js
  references/  signature.md  board.md  harness.md  source-page.md
tests/          the pytest suite of fd (not shipped)
assets/         the README pictures and their HTML sources (pack readme-design)
docs/baseline/frontdoor/
docs/baseline/readme-design/
```

## What loads when

| Surface | Loads | Holds |
|---|---|---|
| `description` frontmatter | always | the trigger phrases |
| `SKILL.md` body | when the skill runs | the ordered workflow and the rules an agent might argue away |
| `references/*.md` | when the body says to read one | platform facts, checklists, patterns |
| `scripts/*.py` | executed, not read | the repeatable mechanics |

## Execution flow

| Skill | Flow |
|---|---|
| `frontdoor-readme` | classify greenfield or brownfield -> fact list and questions -> signature and hero (rough directions on the local board) -> propose the plan, wait for approval -> image building by `frontdoor-illustrate` when available -> write the complete README -> verify -> record |
| `frontdoor-illustrate` | find the brand -> find the signature (rough directions for a new repository, on the local board) -> set up the source folder from the starter -> write one `.item` per image -> `render.py` -> look at every image, compute contrast -> report |
| `frontdoor-landing` | existing-landing check -> ask placement -> learn brand and rules -> two or three rough directions on the local board -> build `index.html` -> preview image -> `shoot.py` and `lighthouse.py` -> report |
| `frontdoor-ui-gallery` | read the rules and the stack (one backend and one frontend reference) -> find the seam, install, generate bindings -> list the states in `gallery.json` -> typed mocks and a gallery dev config -> `shoot.py render` -> look, confirm observations in the DOM -> `real.ps1` on the built app -> type check, build, `shoot.py check` -> report |

## Scripts

| Script | Input | Output |
|---|---|---|
| `render.py` | a source page, a root to serve, an output folder | `<id>.webp` and `<id>-dark.webp` per `.item`, the fonts and grounds found; exit 1 on a clipped item, a file over the size budget, a requested font that did not load, or a stylesheet that still carries the starter marker |
| `contrast.py` | color pairs | the WCAG ratio of each pair and PASS, LARGE-ONLY or FAIL; exit 1 under 4.5 |
| `shoot.py check` | a folder to serve, a page, optional `--click` selectors | full-page PNGs per width and scheme, FAIL and WARN lines, with `--click` a FAIL for a control whose click changes nothing with or without reduced motion, exit 1 on any FAIL |
| `shoot.py og` | a page | a 1200x630 PNG |
| `lighthouse.py` | a folder to serve, a page, a preset | the four category scores and the audits that lost points |
| `frontdoor-ui-gallery/scripts/shoot.py render` | a `gallery.json` and a running gallery dev server | `shots/<id>-<theme>.webp` and `gallery-data.js` beside it; exit 1 on a page error, a missing or ambiguous action target, or a crop that finds less than it names |
| `frontdoor-ui-gallery/scripts/shoot.py check` | a gallery folder | screenshots at 390 and 1440 px in both schemes, outside the repository; FAIL on a page error, a missing or broken image, horizontal overflow |
| `frontdoor-readme/scripts/animate.py` | a source page with a global drawing function, an item id, a `--call` holding `{v}`, an output folder; or `--batch` with a JSON list of such jobs | `<name>.webp` and `<name>-dark.webp` as looping animated WebP, or `<name>.draft.webp` with `--draft`; each file size and the seconds since start; exit 1 on a file over `--max-kb`, a missing item id or a failed job |
| `real.ps1` | an open window's title, an output path, a pattern to hide | a PNG of the window with matching text painted over (Windows) |
| `board.py add` / `build` / `choose` | the `.frontdoor` folder of the repository, a round file, or a round and direction ids | `directions.json` (every round) and `directions.html` (the board, newest round first); `.frontdoor/` added to `.gitignore`; the board opened in the default browser; exit 1 on a missing file, a path outside the folder, an unknown or repeated direction id |
| `frontdoor-core/scripts/fd.py` (`fd`) | a command: `page`, `round`, `choose`, `status`, `board`, `render`, `animate`, `contrast`, `daemon` | the board in `.frontdoor/board/` (`board.json`, `board-data.js`, `index.html`, a folder per page, round and variant), renders as `render.py` writes them plus the `data-finish` modes, the daemon state in `.frontdoor/fd-daemon.json`; exit 1 on a failure or a render WARN, 2 on a wrong argument |

`fd` (FD-D41):

| Part | What |
|---|---|
| `fdlib/board.py` | the board record: pages with free slugs, rounds numbered per page, a draft per `round new` and a published round per `round add`, pictures paired by file name (`<name>`, `<name>-light`, `<name>-dark`, `.draft`), images taken from `<variant>/out/` when it exists, `index.html` linked unless `links` is given, every path checked to stay inside the board; each round's `choice` holds `chosen`, `note`, `notes` (one per variant id) and `date`, written by `fd choose`, which also reads the board's copied text from its last `fd-choice {json}` line (`--from`) |
| `assets/board.html` | the board page, copied unchanged to `.frontdoor/board/index.html`; reads `window.FD_BOARD` from `board-data.js`; routes on `#/<page>/<round>/<variant>[/view/<n>]` and `#/<page>/<round>/compare/<a>/<b>`, pushing history on a round or page change; keeps the picture theme, the viewer zoom, the last place and each round's picks and notes in `localStorage` under a key prefixed with the page path, dropping a round's local picks when `board.json` records a newer choice; copies the choice to the clipboard, with a text box fallback |
| `fdlib/render.py` | `Renderer`: one browser, one static server per served root (`Cache-Control: no-store`, so a long-lived browser sees edits), the item checks of `render.py`, an encode submitted to a process pool as each item is captured (no pool for a single picture), lossless WebP at method 4 |
| `fdlib/daemon.py` | a single-threaded HTTP server on 127.0.0.1 holding a `Renderer` with a warm pool; a random token in `.frontdoor/fd-daemon.json`; started detached (breaking away from the caller's job object on Windows when allowed); stops after `--idle` seconds; `fd render` falls back to its own process when it does not answer |
| `fdlib/cli.py` | argparse commands; `animate` and `contrast` are routed before parsing and run the imported `animate.py` and `contrast.py`, so their own options pass through and their worker processes can import their functions |
| `--watch` | polls the served root every 0.4 s for changed HTML, CSS, JS, SVG, JSON and font files and renders again with the same browser |

`animate.py` pipeline (FD-D35):

| Stage | Where | What |
|---|---|---|
| Capture | main process, Playwright async, up to 4 pages at once | one page per job and theme; per frame the call, then loaded images and two `requestAnimationFrame`; the element screenshot kept as PNG bytes; a value already captured (the sine gives each sway value twice) reused |
| Finish | worker | resize to `--size` (or 600 px wide for `--draft`), then rounded corners and the `--cardline` border, radius 24 and border 3 scaled by output / native width; masks built once per size per worker |
| Encode | worker, `--workers` processes (default the CPU count), submitted as each frame is captured | the rectangle that changed since the previous frame, offsets even; unchanged 8x8 blocks made transparent and blended, unless a changed block holds a partly transparent corner pixel; an unchanged frame merged into the previous frame's duration |
| Mux | main process | `RIFF`/`WEBP` with `VP8X` (alpha, animation), `ANIM` (transparent background, loop forever) and one `ANMF` per frame holding the still's `ALPH` and `VP8 ` chunks; written to `<file>.part`, then renamed |

`--draft` keeps the loop length (frames / fps of the real file) over at most 12 frames, at method 2 and quality 50, with no size limit; durations are spread so the frames sum to the loop length exactly.

They run as `uvx --from playwright --with pillow python -I <script> ...` (`render.py`, `animate.py`), `uvx --from playwright python -I <script> ...` (`shoot.py`) or `uvx python -I <script> ...` (`lighthouse.py`, `contrast.py`, `board.py`), and take the browser from the machine. `board.py` is the same file in all three skills and uses only the standard library; it does not start a browser itself beyond handing the page to the operating system.

## Source page contract

| Rule | Reason |
|---|---|
| each image is a `.item` with a unique id inside `.sheet` | the id is the output file name |
| `.item` is 1200 CSS px wide with `zoom: 2` | the image is 2400 px, twice the density of a README column |
| theming only through `html[data-theme="dark"]`, set from `?theme=` | `render.py` opens the page once per theme |
| `--cardline` defined in both themes | the finishing step draws it as the border |
| the `--starter-placeholder` line deleted from the stylesheet | while it is served, `render.py` warns that the starter's values are in use |
