---
baseline_schema: "2.0"
pack: "ui-gallery"
document: "introduction"
status: "active"
updated: "2026-10-22"
code_ref: "uncommitted"
---

# UI gallery: Scope, Current Truth, Target

## Scope

How the `frontdoor-ui-gallery` skill of this repository was crafted, seen from this repository: where the workflow came from, the decisions that shaped the skill, the trials that tested it, and the state it left in the repositories it ran on. The skill catalogues every view and state of an app's UI by rendering the app's real frontend with its backend calls mocked, and writes a review page (UG-D1).

The workflow was not designed here. It was built by hand inside the `docker-zero` repository (https://github.com/the-khiem7/docker-zero), a Windows tray app in Go with Wails v3 and Svelte, as item 2 of that repository's design phase, then packaged into this repository on the user's request. `docker-zero` stays the reference instance of a gallery (UG-D7): when this pack says "docker-zero" it means that repository, read from its working copy beside this one; paths given for it are relative to its root.

In scope: the skill folder `frontdoor-ui-gallery/`, its trials on three apps, the gallery files the skill left in those apps, and the documentation of the skill in this repository. Out of scope: the redesign of any app's UI (in `docker-zero` that is items 3 and 4 of its own design phase), and the README pictures of this repository (pack `readme-design`, RD-D4).

The general rules for every frontdoor skill stay in the `frontdoor` pack; that pack points here for this skill.

## Current truth

| Item | State |
|---|---|
| Skill | `frontdoor-ui-gallery/` at this repository's root, uncommitted; `quick_validate` passes; layout in `ui-gallery.sourcecode.md` |
| Reference instance | `docker-zero`: gallery in `design/ui-gallery/`, mocks in `frontend/gallery/`, dev config `frontend/vite.gallery.config.ts`, 5 views, 51 states, 4 real references, committed there (`84ba537`, `94af686`, `9c4baf1`, `a76cea7`) |
| Trial instance, Wails v3 `beta.8` + Vue 3 | `Remotune` (https://github.com/the-khiem7/Remotune): 2 views, 29 states, uncommitted in that working tree |
| Trial instance, Tauri v2 + Vue 3 | `IRYS-desktop` (https://github.com/the-khiem7/IRYS-desktop): 3 views, 19 states, uncommitted in that working tree |
| Frontdoor documentation | `AGENTS.md`, `README.md` and four README pictures updated for the skill, uncommitted (roadmap Phase 6) |
| `docker-zero`'s own pack | its roadmap (`docs/baseline/docker-zero/docker-zero.roadmap.md`, Phase 10 item 2) and DZ-D28 describe the hand-built inventory under its old paths `design/ui-inventory/` and `frontend/inventory/`; the move onto the skill is not recorded there yet (roadmap Phase 7) |

Observed running on Windows with Edge, 2026-10-22: the skill's `shoot.py render` reproduced `docker-zero`'s 50 hand-built states at the same image sizes; two fresh agents given only the skill folder built the `Remotune` and `IRYS-desktop` galleries; `shoot.py check` reported 0 FAIL on all three galleries.

Not observed: the skill chosen by a host from a plain request (FD-Q1); a React, Electron or plain web frontend; macOS or Linux (FD-Q3); screenshots of the built app for `Remotune` or `IRYS-desktop`; any mock checked against a running backend.

## Target

A person asks "show me every screen of this app" in a Wails, Tauri or Vite repository with the skill installed, and gets a committed `design/ui-gallery/` with every state in light and dark, confirmed observations and a review page, without the skill being changed and without any dependency added to the app.

## Constraints

| Constraint | Reason |
|---|---|
| The skill runs alone from its own folder (FD-D2) | a skill installed alone must not point at a folder that is not there |
| The gallery page keeps one neutral look (UG-D2) | it is a development tool; the user chose neutral over a repository signature |
| Galleries are committed in the app's `design/ui-gallery/` (UG-D3) | a redesign is judged against the states before it |
| Stack references are split by pillar, backend and frontend (UG-D4) | the user asked for one file per framework |
| No dependency is added to an app and no lock file changes | two of the three apps forbid dependencies added for visual work; a lock file is shared state |
| The skill writes files and stops; commits in this repository go through `commit-composer-max`, push stays with the owner (UG-D9) | the user's instruction |
| Nothing personal in a committed gallery: placeholders such as `you`, account paths painted over in real screenshots | `docker-zero` is public and forbids user names and absolute user paths |
