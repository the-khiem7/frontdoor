---
baseline_schema: "2.0"
pack: "frontdoor"
document: "sourcecode"
status: "active"
updated: "2026-10-12"
code_ref: "uncommitted"
---

# Frontdoor: Topology and Execution Flow

## Folders

```text
frontdoor-readme/
  SKILL.md
  agents/      openai.yaml
  scripts/     board.py
  references/  github-readme.md  audit-and-plan.md  readme-content.md  signature.md
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
  references/  existing-landing.md  pages-setup.md  page-craft.md  verify.md  signature.md
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

## Scripts

| Script | Input | Output |
|---|---|---|
| `render.py` | a source page, a root to serve, an output folder | `<id>.webp` and `<id>-dark.webp` per `.item`, the fonts and grounds found; exit 1 on a clipped item, a file over the size budget, a requested font that did not load, or a stylesheet that still carries the starter marker |
| `contrast.py` | color pairs | the WCAG ratio of each pair and PASS, LARGE-ONLY or FAIL; exit 1 under 4.5 |
| `shoot.py check` | a folder to serve, a page | full-page PNGs per width and scheme, FAIL and WARN lines, exit 1 on any FAIL |
| `shoot.py og` | a page | a 1200x630 PNG |
| `lighthouse.py` | a folder to serve, a page, a preset | the four category scores and the audits that lost points |
| `board.py add` / `build` / `choose` | the `.frontdoor` folder of the repository, a round file, or a round and direction ids | `directions.json` (every round) and `directions.html` (the board, newest round first); `.frontdoor/` added to `.gitignore`; the board opened in the default browser; exit 1 on a missing file, a path outside the folder, an unknown or repeated direction id |

They run as `uvx --from playwright --with pillow python -I <script> ...` (`render.py`), `uvx --from playwright python -I <script> ...` (`shoot.py`) or `uvx python -I <script> ...` (`lighthouse.py`, `contrast.py`, `board.py`), and take the browser from the machine. `board.py` is the same file in all three skills and uses only the standard library; it does not start a browser itself beyond handing the page to the operating system.

## Source page contract

| Rule | Reason |
|---|---|
| each image is a `.item` with a unique id inside `.sheet` | the id is the output file name |
| `.item` is 1200 CSS px wide with `zoom: 2` | the image is 2400 px, twice the density of a README column |
| theming only through `html[data-theme="dark"]`, set from `?theme=` | `render.py` opens the page once per theme |
| `--cardline` defined in both themes | the finishing step draws it as the border |
| the `--starter-placeholder` line deleted from the stylesheet | while it is served, `render.py` warns that the starter's values are in use |
