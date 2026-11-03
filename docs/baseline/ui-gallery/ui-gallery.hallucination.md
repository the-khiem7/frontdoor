---
baseline_schema: "2.0"
pack: "ui-gallery"
document: "hallucination"
status: "active"
updated: "2026-10-22"
code_ref: "uncommitted"
---

# UI gallery: Decisions and Open Questions

UG-D1 to UG-D5 were first written as FD-D26 to FD-D30 in the `frontdoor` pack and moved here; those numbers stay reserved there.

## Entry index

One row per entry. A row states what the entry is about and nothing more. An answer that turns on an entry whose full text was not read is unbacked.

| Entry | About | Status | Related |
|---|---|---|---|
| UG-D1 | a fourth frontdoor skill that catalogues an app's UI states from a mocked frontend, and its origin in `docker-zero` | current | FD-D1, FD-D2, UG-D7 |
| UG-D2 | the gallery page keeps one neutral look, an exception to FD-D17 | current | FD-D17, UG-D1 |
| UG-D3 | where a gallery lives: committed in `design/ui-gallery/` of the app's repository | current | FD-D24, UG-D1 |
| UG-D4 | stack references split into two pillars, backend and frontend | current | UG-D1 |
| UG-D5 | how the gallery mocks and shoots a state: narrowest seam, typed mocks, paused timers, pointer moved off | current, lesson | UG-D1, UG-D4 |
| UG-D6 | the skill's name | current | FD-D14 |
| UG-D7 | `docker-zero` as the reference instance, moved onto the skill's files | current | UG-D1, UG-D3 |
| UG-D8 | how the skill was trialled on `Remotune` and `IRYS-desktop` | current | UG-D1, UG-Q1 |
| UG-D9 | delivery: README pictures with the skill, commits through `commit-composer-max`, push by the owner | current | RD-D4 |
| UG-D10 | another agent session working in `docker-zero` at the same time | current, lesson | UG-D7 |
| UG-Q1 | what happens to the uncommitted trial galleries | open | UG-D8 |

## UG-D1: a fourth skill, `frontdoor-ui-gallery`, catalogues every UI state from a mocked frontend

Decision: add `frontdoor-ui-gallery`, which renders an app's real frontend in a browser with its backend calls replaced by fixed data per state, screenshots every view and state in light and dark, records confirmed UI defects, pairs a few states with screenshots of the built app, and writes one review page - a redesign needs every state on screen, and most of them (first run, each error, a busy call, a confirmation) cannot be reached by hand on a working machine.

Origin: the workflow was built by hand in `docker-zero` as item 2 of that repository's design phase (Phase 10 in its pack, `docs/baseline/docker-zero/docker-zero.roadmap.md`; its method is DZ-D28 there), and packaged here at the user's request ("This workflow are excelence. Pack this workflow into an skill of the frontdoor family"). As first built in `docker-zero` (commit `84ba537`):

- `frontend/vite.inventory.config.ts`, a Vite config whose `resolveId` plugin swapped the six generated Wails service modules for mocks in `frontend/inventory/mock/`, each written as `satisfies Mocked<typeof Real>`;
- `frontend/inventory/fixtures.ts`, scenarios picked by `?state=`, with calls that resolve, reject with the Go error text, or hang;
- `design/ui-inventory/shoot.py`, a hard-coded list of 50 states rendered with Playwright on the installed Edge at 2x in light and dark, cropped to the window, the full scroll height or named cards;
- `design/ui-inventory/real.ps1`, `PrintWindow` captures of the installed exe with account paths painted over through UI Automation;
- `design/ui-inventory/index.html`, the review page with Keep / Revise / Discuss, notes kept in the browser and Copy review as Markdown;
- 10 observations, one confirmed by measuring the DOM (a failed Start in the corner box shows nothing: the error line is squeezed to zero height).

What breaks if ignored: a redesign planned from a few hand screenshots misses the error and edge states, which is where the trials found most of their defects (10, 18 and 15 observations in the three apps).

Rejected: part of `frontdoor-illustrate` - that skill renders HTML a person writes as a picture; this one runs an app's own frontend against mocks, with its own trigger and scripts. Part of `frontdoor-landing` - a landing page is a public face, the gallery a working tool. Screenshots of the built app only - most states need real conditions (an uninstall, a blocked network, a stopped service) and cannot be repeated after each redesign.

## UG-D2: the gallery page keeps one neutral look

Decision: `assets/gallery.html` ships one fixed, neutral page design, used unchanged in every repository; it is the one exception to FD-D17 - the page is a tool for the people building the app, read beside the app's own screenshots, and a repository signature on it would compete with the UI under review.

What breaks if ignored: each gallery needs a signature run first, and a strongly styled page frames the screenshots in a look that is not the app's.

Rejected: the repository's signature - the user chose a neutral page because the gallery is for development use.

## UG-D3: a gallery lives in `design/ui-gallery/`, committed

Decision: the skill writes `gallery.json`, `index.html`, `gallery-data.js`, `shots/` and `real/` to `design/ui-gallery/` of the app's repository, for the user to commit, and the mock harness to a `gallery/` folder inside the frontend's source - a redesign is judged against the states before it, which needs the old gallery in the history.

What breaks if ignored: a gallery kept in an ignored folder is gone when the redesign is reviewed; the before and after cannot be compared.

Cost accepted: a full render of 20 to 50 states in two themes is 2 to 4 MB, and every re-render adds that again to the history.

Rejected: `.frontdoor/`, ignored by git like the boards of rough directions (FD-D24) - those are scratch, the gallery is the record a redesign is measured against; the user chose the committed folder.

## UG-D4: stack references are split into two pillars, backend and frontend

Decision: `references/stacks/` holds one file per backend (`wails3.md`, `tauri2.md`) and one per frontend framework (`svelte.md`, `vue.md`), and `stacks/index.md` names the pair to read and the combinations run so far - the user asked for one reference file per framework, and an app is always one of each.

What breaks if ignored: one file per combination repeats every backend rule in each frontend file, and the copies drift; a new framework (React) would need a file per backend.

Rejected: one file per combination (`wails3-svelte.md`, `wails3-vue.md`, `tauri2-vue.md`) - repetition, as above. One generic reference - the seams differ (generated bindings, an app wrapper, `invoke` with string errors) and an agent guessed wrong where none was written.

## UG-D5: how a state is mocked and shot

Decision:

- Replace the narrowest module the frontend calls the backend through: the app's own wrapper, else the generated bindings, else the platform package; keep the backend's types real.
- Type every mock against the real module (`satisfies Mocked<typeof Real>` in `mock-kit.ts`), so a changed backend fails the frontend's type check.
- Serve the mocks from a separate dev config that the production build never reads, and check the built bundle for fixture text.
- Reject a failed call the way the backend does (`rejectWith`), and keep what a command changes in an in-memory `store` so a success state agrees with itself.
- Shoot on a paused fake clock when the app's own timers move a state on (`"timers": "paused"`), grow the window until a scroller under fixed chrome no longer scrolls, and move the pointer off the page before each shot.

Why: each rule answers a failure seen in the three runs.

Lessons from the runs, 2026-10-22:

| Seen | Fix |
|---|---|
| A full-height shot cut off the bottom, and after a click the top, when the scroller sat below a 34 or 48 px title bar | the window grows until the scroller no longer scrolls, title bars included, and the scroller is scrolled to the top first |
| A poll every 1.5 s cleared a command's error about 0.7 s after it appeared, so error shots were racy | `"timers": "paused"` advances fake timers only by each wait's length |
| A success notice stood beside controls showing the old value | the scenario file's `store` |
| Tauri rejects `invoke` with a bare string; an `Error` made the UI print `Error: ...` | `rejectWith: "string"` |
| Two radio groups shared labels, number fields shared the label "minutes", a switch had no name | `within`, `nth` and `selector` on an action |
| The pointer left on the Start tile shot a hover style in which the white label vanished on a light tile, in two of `docker-zero`'s states | the pointer is moved off the page after the last action; a hover state is its own state with `keepHover` (`docker-zero` now has one) |
| `--only` kept old titles and notes | texts always come from `gallery.json`; only images are kept |
| A dev server stopped as a shell task kept running and held the folder open | the skill says to end the node process |

Rejected: `@tauri-apps/api/mocks` `mockIPC` as the default for Tauri - its event mocking was not confirmed on the installed version, and an app wrapper gives typed mocks. Storybook or a mock-service package - a new dependency, which two of the three repositories forbid adding for visual work. Racing app timers with short waits - shots differed between runs.

Not verified: the mocks against a running backend (each run checked error texts by reading the backend source); React or Electron frontends; macOS and Linux (FD-Q3); real-app screenshots outside Windows.

## UG-D6: the skill is named `frontdoor-ui-gallery`

Decision: name the skill `frontdoor-ui-gallery` - the family prefix of FD-D14; the request spelled it `frontfoor-ui-gallery`, a typing slip the user corrected.

What breaks if ignored: a skill outside the family prefix is not found next to its siblings and breaks `npx skills add --skill frontdoor-*` habits.

Rejected: the name as typed - a typing slip.

## UG-D7: `docker-zero` is the reference instance and runs on the skill's own files

Decision: move `docker-zero`'s hand-built inventory onto the skill's layout: `design/ui-inventory/` renamed `design/ui-gallery/`, `frontend/inventory/` renamed `frontend/gallery/`, `frontend/vite.inventory.config.ts` renamed `vite.gallery.config.ts`, the state list moved from `shoot.py` into `gallery.json`, and `shoot.py` and `real.ps1` removed from that repository because the skill ships them; the move must reproduce every state at the same image size (commit `94af686` there) - the user wants the redesign's re-shoot to use the same tool as every other project, and a second copy of the scripts in `docker-zero` would drift from the skill.

What breaks if ignored: `docker-zero` keeps an older renderer than the one the other apps get, and its gallery cannot take the fixes the trials produced.

Observed after the move: 50 states with the same sizes; after the Phase 5 fixes a 51st state, `popup-start-hover` (commit `9c4baf1`), and a re-shoot of the 21 clicked states in which 19 came out byte-identical and 2 lost a hover artifact (commit `a76cea7`).

Rejected: keep `docker-zero`'s own scripts beside the skill - two copies of the renderer. Keep the folder name `ui-inventory` - the skill names the folder `ui-gallery` everywhere.

## UG-D8: trials run by fresh agents directly in the trial repositories, results left uncommitted

Decision: test the skill with one fresh agent per app, given only the skill folder, working directly in the working tree of `Remotune` and of `IRYS-desktop` (both pulled first, both clean), with the results left uncommitted for their owner - the user asked for direct runs instead of temporary worktrees, and a run by the skill's author would follow memory, not the text.

Allowed in those trees, by the user: installing frontend dependencies with `npm install --no-package-lock` because the repositories' `bun` is not installed, so no lock file changed; generating `Remotune`'s gitignored Wails bindings with the pinned `v3.0.0-beta.8` through `go run`, not the installed `beta.30` CLI; gallery dev servers on ports 9247 and 9248 so the runs did not collide; screenshots of an app already running, without restarting or reconfiguring it.

What breaks if ignored: a trial by the author hides every gap the text leaves; a worktree the user did not ask for adds a cleanup step.

Rejected: git worktrees - the user said to run directly on the repositories. Deleting the trial output after the report - the user wants to look at it first (UG-Q1).

## UG-D9: delivery: README pictures in the same delivery, commits through `commit-composer-max`, push by the owner

Decision: update this repository's README, pictures and `AGENTS.md` in the same delivery as the skill (RD-D4 in the `readme-design` pack), commit in this repository one verified step at a time through the `commit-composer-max` skill, and leave every push to the owner - the user's answers to the packaging plan.

What breaks if ignored: a README that lists the other skills only, or a commit history that no agent can audit without reading the diff.

Rejected: README pictures in a later phase - the user chose the same delivery.

## UG-D10: Lesson: another agent session worked in `docker-zero` at the same time

Decision: in a repository another session may be changing, stage and commit only this task's paths with `git commit -- <paths>`, check `git status` and `git log` right before each commit, and leave that session's files (its pack edits, `.github/`, `AGENTS.md`, `design/brand/`) alone, even when this task's own record belongs in one of them.

Why: while the skill was being packaged, a second session in `docker-zero` replaced the app icon, built a logo gallery in `design/brand/gallery/`, wrote a release workflow and edited that repository's pack and `AGENTS.md`; between two commands of this task its git activity unstaged the renames staged for `94af686`, which then showed as unstaged deletions.

What breaks if ignored: a commit that sweeps up another session's half-done work, or a pack edit that overwrites theirs.

Also seen: a gallery dev server stopped as a background shell task kept its node process alive and held `frontend/inventory` open, so `git mv` failed with "Permission denied" until the process was ended by id; the skill's pitfalls now say to end the node process.

Rejected: nothing; these were process mistakes and their fixes.

## Open questions

### UG-Q1: what happens to the trial galleries in `Remotune` and `IRYS-desktop`?

Both were made before the Phase 5 fixes and sit uncommitted in those working trees, with their mock folders, dev configs and the `gallery` scripts. Committing them meets each repository's rules: `Remotune` puts code and its pack update in one commit and forbids code comments; in `IRYS-desktop` the CI `biome check .` would lint `design/ui-gallery/` and fail. What is at stake: dropped galleries waste two finished catalogues of 18 and 15 observations; committed as they are, they carry the older renderer's output. Trigger to close: the owner reviews the two pages and says keep (re-render with the fixed skill, then commit under each repository's rules) or remove.
