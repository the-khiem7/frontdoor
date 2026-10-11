---
baseline_schema: "2.0"
pack: "readme-design"
document: "sourcecode"
status: "active"
updated: "2026-10-11"
code_ref: "uncommitted"
---

# README design: Topology and Execution Flow

## Folders

```text
assets/
  source/      readme.html  scenes.html  shared.css  shared.js
  <id>.webp  <id>-dark.webp   for hero, skills-map, readme-flow, illustrate-flow, landing-flow, scene-readme, scene-illustrate, scene-landing
README.md      references the pictures by relative path
docs/baseline/readme-design/
```

The render script and the starter these sources came from live in `frontdoor-illustrate/` (pack `frontdoor`).

## Execution flow

Run from the repository root; each command renders one source page in both themes into `assets/`.

| Source page | Command |
|---|---|
| `readme.html` | `uvx --from playwright --with pillow python -I frontdoor-illustrate/scripts/render.py assets/source/readme.html --root assets --out assets` |
| `scenes.html` | `uvx --from playwright --with pillow python -I frontdoor-illustrate/scripts/render.py assets/source/scenes.html --root assets --out assets` |

`--items id1,id2` renders a subset. The command sits in each page's header comment.

## Source pages

| Page | Items | How a figure is built |
|---|---|---|
| `readme.html` | `hero`, `skills-map`, `readme-flow`, `illustrate-flow`, `landing-flow` | HTML cards; flow items place `.step` cards absolutely over an svg of `.w` connectors, with arrowhead markers `#ah` and `#aa` |
| `scenes.html` | `scene-readme`, `scene-illustrate`, `scene-landing` | one inline svg per item, 1200 x 600 CSS px, plus HTML tags and a heading; shared shapes `#spark` and `#plant` defined once in `<defs>`; a small script draws the text-like lines |

`shared.css` holds the theme tokens for both pages. The scene palette adds `--ground`, `--sage`, `--sage-soft`, `--sky`, `--sky-2` and `--code` to the base tokens. The light and dark pictures drawn inside a scene use fixed colors.

The general source-page contract (unique `.item` ids, 1200 CSS px with `zoom: 2`, theming through `html[data-theme="dark"]`, `--cardline` in both themes) is in the frontdoor pack's sourcecode.

## What each picture restates

| Picture | Restates | Stale when |
|---|---|---|
| `skills-map` | the skills table and the optional-help rule | a skill is added or removed, or a sibling becomes a prerequisite |
| `readme-flow`, `illustrate-flow`, `landing-flow` | the steps of the matching `SKILL.md` | a step, gate or branch of that skill changes |
| `scene-*` | what each skill takes in and puts out, and the stop-and-ask sign | a skill's job or its landing-page check changes |
| `hero` | the lead sentence and its product areas | the lead sentence changes |
