---
baseline_schema: "2.0"
pack: "readme-design"
document: "roadmap"
status: "active"
updated: "2026-10-11"
code_ref: "uncommitted"
---

# README design Roadmap

Reasoning for every row below lives in `readme-design.hallucination.md` under the entry named in its Basis column. Do not restate it here.

## Status by area

| Area | Basis | Status | Evidence |
|---|---|---|---|
| Pictures rendered from HTML into `assets/` | RD-D1 | implemented | both source pages render with exit 0 and no WARN; sixteen files |
| Look | RD-D2 | implemented | every image looked at in light and dark; contrast computed, lowest 5.15 |
| A scene per skill, flows in `<details>` | RD-D3 | implemented | README shows each scene first and each flow under `<details>` |
| README on github.com | RD-Q1 | unobserved | not opened on the hosting site |
| Root `assets/` and `npx skills add` | RD-Q2 | unobserved | not re-run after the folder was added |

## Phase 1: the first picture set

Acceptance criteria:

- a hero, a skills map and a step-box flow per skill, each in a light and a dark theme
- each statement in a picture traced to the README or a `SKILL.md`
- `render.py` exits 0 with no WARN and every file is under 300 KB

### Checkpoint: complete

| Item | Result |
|---|---|
| Figures | `hero`, `skills-map`, `readme-flow`, `illustrate-flow`, `landing-flow`: ten files of 59 to 90 KB, about 720 KB |
| Render | `render.py` exit 0, no WARN; every image looked at in both themes |
| Contrast | 13 text color pairs computed; lowest 5.57 |
| Skill text | `frontdoor-readme` step 4 and `description` reworded so the render skill is optional (FD-D16, pack frontdoor) |

## Phase 2: a scene per skill

Acceptance criteria:

- three scenes, each in a light and a dark theme, each statement traced to the README or a `SKILL.md`
- the README shows each scene first and keeps each flow inside `<details>`
- every image path in the README exists, and no skill count appears in text or images

### Checkpoint: complete

| Item | Result |
|---|---|
| Scenes | `scene-readme`, `scene-illustrate`, `scene-landing`: six files of 92 to 122 KB, about 630 KB |
| Render | `render.py` exit 0, no WARN; every image looked at in both themes |
| Contrast | text color pairs computed for both pages; lowest 5.15; the code-window string color was lightened from 4.22 and not recomputed |
| README | rewritten with the scenes; all sixteen image paths exist; `<details>` tags balance; no non-ASCII character; no skill count in text |
| Not observed | the README on github.com (RD-Q1) |

## Risks

| Risk | Detail |
|---|---|
| A picture goes stale when a `SKILL.md` step or the set of skills changes | RD-D1 |
| A render without network puts fallback fonts into the images | RD-D1 |
| The README does not render as designed on the hosting site | RD-Q1 |
| `npx skills add` picks up the root `assets/` | RD-Q2 |

## Next action

1. Open the README on a pushed branch or the repository page in light and dark and on a phone, and record the result (RD-Q1).
2. After `assets/` is pushed, run `npx skills add <repository> --list` and a single-skill install, and record whether the folder is skipped (RD-Q2).
3. When a `SKILL.md` step or the set of skills changes, edit the matching source page under `assets/source/` and render it again (RD-D1).
4. Commit only when asked.
