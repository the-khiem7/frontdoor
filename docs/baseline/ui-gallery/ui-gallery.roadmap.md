---
baseline_schema: "2.0"
pack: "ui-gallery"
document: "roadmap"
status: "active"
updated: "2026-10-22"
code_ref: "uncommitted"
---

# UI gallery Roadmap

Reasoning for every row lives in `ui-gallery.hallucination.md` under the entry named in its Basis column. Commits named here are in `docker-zero` unless a row says otherwise; nothing in this repository is committed yet.

| Phase | Depends on | Status | Acceptance |
|---|---|---|---|
| Phase 1 | - | complete | The workflow runs by hand in `docker-zero` |
| Phase 2 | Phase 1 | complete | Packaging plan approved by the user |
| Phase 3 | Phase 2 | complete | Skill built; `docker-zero` reproduced by the skill's script |
| Phase 4 | Phase 3 | complete | Fresh agents build galleries for a Wails v3 + Vue and a Tauri v2 + Vue app |
| Phase 5 | Phase 4 | complete | Every trial finding fixed or recorded; `docker-zero` re-run |
| Phase 6 | Phase 5 | active | This repository's README, pictures, `AGENTS.md` and packs describe the skill |
| Phase 7 | Phase 6 | planned | Committed here; `docker-zero`'s pack records the move; trial galleries settled |

## Phase 1: the workflow, by hand in `docker-zero`

Status: complete. Built as item 2 of `docker-zero`'s design phase (its pack: Phase 10 item 2, DZ-D28) and committed there as `84ba537` (the inventory) and `4bcf8d9` (its pack record). Basis: UG-D1.

| Check | Result |
|---|---|
| Render | 50 states over popup, corner box, settings, maintenance and setup, light and dark, 4.4 MB of WebP |
| Real references | popup, corner box, settings and setup of the installed exe, account paths painted over |
| Page | filters, reviews kept in the browser, Copy review; no page error at 1440 px light and dark, no horizontal scroll at 390 px |
| Observations | 10 on the page, among them the corner box's invisible error, confirmed by measuring the DOM |
| `docker-zero` checks | `wails3 task lint` 0 issues, `wails3 task test` ok, `wails3 task build` ok with no mock in the production bundle |

## Phase 2: the packaging plan

Status: complete. The user named the skill and answered the plan's questions: name (UG-D6), committed output folder (UG-D3), neutral page (UG-D2), Vite frontends with one reference per framework and the two pillars (UG-D4), trial repositories and direct runs (UG-D8), `docker-zero` moved onto the skill (UG-D7), README pictures in the same delivery and commits through `commit-composer-max` (UG-D9).

Surveyed before building, by two read-only agents:

| App | Seam found | Facts that shaped the skill |
|---|---|---|
| `Remotune` | one wrapper, `frontend/src/wails.ts`, re-exporting one service module | Wails `beta.8` against the installed `beta.30` CLI; bindings gitignored and absent; a 1.5 s poll; no comments allowed in code |
| `IRYS-desktop` | one wrapper, `src-vue/lib/ipc.ts`, with 9 `invoke` commands, plus `listen("irys://tick")` | two HTML entries; a transparent full-screen break window; theme from `localStorage`; a clock-driven greeting; no dependencies for visual work |

## Phase 3: the skill, and `docker-zero` on it

Status: complete. Skill files as in `ui-gallery.sourcecode.md`; `quick_validate` passes. `docker-zero` moved onto the skill's layout in `94af686` (UG-D7): the same 50 states at the same image sizes; `shoot.py check` 0 FAIL; lint, test and build pass there, with no fixture text in `frontend/dist`.

## Phase 4: trials by fresh agents

Status: complete. Basis: UG-D8.

| App | Result |
|---|---|
| `Remotune` (Wails v3 `beta.8`, Vue 3) | 2 views, 29 states, 3.9 MB, 18 observations; mocked through the app's wrapper; a mock missing one function failed `vue-tsc`; build clean of fixtures; `check` 0 FAIL; no real screenshots (the app was not running) |
| `IRYS-desktop` (Tauri v2, Vue 3, two HTML entries) | 3 views, 19 states, 2.2 MB, 15 observations; wrapper and event module mocked, transparent break window; a mock missing `quit` failed `vue-tsc`; build clean of fixtures; `check` 0 FAIL; no real screenshots (settings window closed, tray icon in the overflow) |

Both agents stopped their dev servers and left nothing committed. Their findings about the skill, 15 and 15, are the input of Phase 5.

## Phase 5: fixes from the trials, and a re-run

Status: complete. Basis: UG-D5.

| Item | Result |
|---|---|
| Fixes | full-height crop under a title bar, paused timers, per-state `settle`, `within` / `nth` / `selector` / `hover` actions, the pointer moved off before a shot, `--only` refreshing texts, `rejectWith`, a scenario template with a `store`, `skipped` states on the page, a config template that accepts a function config, explicit button types; skill text on lint coverage, lock files, pinned binding generators, line endings, comment stripping, port agreement, single-instance apps |
| Re-run on `docker-zero` | five states on a paused clock at the previous sizes; the reworked renderer exposed a hover defect, recorded as state `popup-start-hover` (`9c4baf1`); the 21 clicked states re-shot, 19 byte-identical and 2 without the hover artifact (`a76cea7`); 51 states; `check` 0 FAIL |
| Validation | `quick_validate` passes; no en or em dash and no CR in the skill folder |
| Not re-run | `Remotune` and `IRYS-desktop` after the fixes (UG-Q1) |

## Phase 6: this repository describes the skill

Status: active, uncommitted.

| Item | State |
|---|---|
| `AGENTS.md` | no skill count; the neutral page named as the exception to "Ship no reusable look"; the gallery scripts in "Changing a script" |
| `README.md` | lead sentence, table row, a section with the scene and the flow, requirements, behaviour and status notes, install example |
| Pictures (`readme-design` pack, RD-D4) | `hero` and `skills-map` redrawn, `scene-ui-gallery` and `ui-gallery-flow` added, rendered in both themes |
| `frontdoor` pack | the skill in its introduction and sourcecode; its decisions moved here (FD-D26 to FD-D30 reserved) |
| `readme-design` pack | RD-D4 and its Phase 4 written; the picture lists in its introduction and sourcecode not yet updated |

## Phase 7: commit and settle

Status: planned.

- Commit this repository's work through `commit-composer-max`, one verified group at a time (UG-D9).
- Record in `docker-zero`'s pack that its inventory moved onto the skill (a revision of its Phase 10 item 2 and of DZ-D28's paths), once the other session working there has committed its pack edits (UG-D10).
- Settle the trial galleries (UG-Q1).
- Ask for a gallery in a plain sentence in a repository that has the skill installed and record whether it is selected (FD-Q1 in the `frontdoor` pack).

## Risks

| Risk | Detail |
|---|---|
| A gallery's mocks drift from the backend's behaviour while still matching its types | UG-D5 |
| Each gallery re-render adds megabytes to the app repository's history | UG-D3 |
| Wails v3 betas change the generated binding layout | UG-D4 |
| A trial gallery committed as it is carries the older renderer's output | UG-Q1 |

## Next action

1. Phase 6: update the picture lists in `readme-design.introduction.md` and `readme-design.sourcecode.md` for `scene-ui-gallery` and `ui-gallery-flow`, then run `packtool check` on the three packs.
2. Phase 7: commit this repository's changes with `commit-composer-max` (authorized), grouped as the skill, the README and pictures, and the packs.
3. Phase 7: when `docker-zero`'s working tree shows no uncommitted pack edits from the other session, record the move there.
4. Ask the owner to settle UG-Q1.
