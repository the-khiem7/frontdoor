---
baseline_schema: "2.0"
pack: "readme-design"
document: "introduction"
status: "active"
updated: "2026-10-11"
code_ref: "uncommitted"
---

# README design: Scope, Current Truth, Target

## Scope

The pictures and the layout around them in this repository's own `README.md`, made with the skills the README describes: a hero, a skills map, and per skill a scene with a step-by-step flow, rendered from HTML into light and dark WebP files.

Out of scope: the skills, their scripts and their decisions (pack `frontdoor`), committing or pushing, and any README text beyond what the layout needs.

## Current truth

Every picture is a pair, `assets/<id>.webp` and `assets/<id>-dark.webp`, regenerated from a source page under `assets/source/` (RD-D1).

| Picture | Source page | Where it sits in the README |
|---|---|---|
| `hero` | `readme.html` | the top, inside the `<h1>` |
| `skills-map` | `readme.html` | under "Skills", above the table |
| `scene-readme`, `scene-illustrate`, `scene-landing` | `scenes.html` | first picture under each skill in "How each skill runs" (RD-D3) |
| `readme-flow`, `illustrate-flow`, `landing-flow` | `readme.html` | inside `<details>` "Step by step" under each scene |

README order: hero and a bold lead sentence; Skills (map, table, one sentence); How each skill runs (scene, one sentence, flow in `<details>`, three times); Install; Requirements; Behaviour to know; Status inside `<details>`. The look is an arched doorway in a paper and a night theme (RD-D2); it is one example of a signature, not a template for other repositories (FD-D17, pack frontdoor). The four pictures that restate the skills were redrawn on 2026-10-12 to match the reworked skills.

Observed running, 2026-10-11, on Windows with Edge:

- `render.py` rendered both source pages in both themes: exit 0, no WARN, sixteen files of 59 to 122 KB.
- Every image was looked at in light and dark; contrast of the text color pairs was computed.
- All sixteen image paths in the README exist, the `<details>` tags balance, and no non-ASCII character or skill count appears in the README.
- `frontdoor-readme` step 4 was reworded so the picture work goes to `frontdoor-illustrate` only when it is available (FD-D16, pack frontdoor).

Not observed: the README on github.com in light and dark and on a phone (RD-Q1), and `npx skills add` after the root `assets/` folder was added (RD-Q2).

## Target

A visitor opens the README, sees in under a minute what the repository is and which skill fits, and the pictures tell a story instead of listing steps. Light and dark both read well, and a change to a skill means one edit to a source page and one command.

## Constraints

| Constraint | Why |
|---|---|
| Every statement in a picture traces to the README or a `SKILL.md` | a figure is where an invented claim hides |
| No skill count in the README text or in a picture | `AGENTS.md` bans it; it goes stale when a skill is added or removed |
| Install and usage commands stay text | they must be copyable |
| Pictures live in the root `assets/`, outside every skill folder | nothing in it travels with `npx skills add` |
| Render with network access | web fonts load from Google Fonts; offline, fallback fonts end up in every image |
| ASCII hyphen only; one paragraph is one line | `AGENTS.md` rules for every file |
| The work stays in the working tree until the user asks for a commit | the skills write files and stop |
