---
baseline_schema: "2.0"
pack: "visual-skills"
document: "sourcecode"
status: "active"
updated: "2026-10-10"
code_ref: "uncommitted"
---

# Visual Skills: Topology and Execution Flow

## Folders

```text
readme-visualization/
  SKILL.md
  agents/      openai.yaml
  references/  github-readme.md  audit-and-plan.md
illustration-render/
  SKILL.md
  agents/      openai.yaml
  scripts/     render.py
  assets/      starter.css  starter.html  shared.js
  references/  source-page.md
landing-pager/
  SKILL.md
  agents/      openai.yaml
  scripts/     shoot.py  lighthouse.py
  references/  existing-landing.md  pages-setup.md  page-craft.md  verify.md
docs/baseline/visual-skills/
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
| `readme-visualization` | audit README, brand and repository rules -> ask what is open -> propose the plan -> hand image building to `illustration-render` -> rewrite the README -> verify -> report |
| `illustration-render` | find the brand -> set up the source folder from the starter -> write one `.item` per image -> `render.py` -> look at every image -> report |
| `landing-pager` | existing-landing check -> ask placement -> learn brand and rules -> two or three rough directions -> build `index.html` -> preview image -> `shoot.py` and `lighthouse.py` -> report |

## Scripts

| Script | Input | Output |
|---|---|---|
| `render.py` | a source page, a root to serve, an output folder | `<id>.webp` and `<id>-dark.webp` per `.item`; exit 1 on a clipped item or a file over the size budget |
| `shoot.py check` | a folder to serve, a page | full-page PNGs per width and scheme, FAIL and WARN lines, exit 1 on any FAIL |
| `shoot.py og` | a page | a 1200x630 PNG |
| `lighthouse.py` | a folder to serve, a page, a preset | the four category scores and the audits that lost points |

All three run as `uvx --from playwright --with pillow python -I <script> ...` (`render.py`), `uvx --from playwright python -I <script> ...` (`shoot.py`) or `uvx python -I <script> ...` (`lighthouse.py`), and take the browser from the machine.

## Source page contract

| Rule | Reason |
|---|---|
| each image is a `.item` with a unique id inside `.sheet` | the id is the output file name |
| `.item` is 1200 CSS px wide with `zoom: 2` | the image is 2400 px, twice the density of a README column |
| theming only through `html[data-theme="dark"]`, set from `?theme=` | `render.py` opens the page once per theme |
| `--cardline` defined in both themes | the finishing step draws it as the border |
