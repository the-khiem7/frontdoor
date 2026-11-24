---
baseline_schema: "2.0"
pack: "frontdoor"
document: "roadmap"
status: "active"
updated: "2026-11-24"
code_ref: "uncommitted"
---

# Frontdoor Roadmap

Reasoning for every row below lives in `frontdoor.hallucination.md` under the entry named in its Basis column. Do not restate it here. The pictures of this repository's README are tracked in the `readme-design` pack.

## Status by area

| Area | Basis | Status | Evidence |
|---|---|---|---|
| Three skills and their split | FD-D1, FD-D2 | implemented | `quick_validate` reported each valid before the move in the next row |
| Layout for `npx skills add` | FD-D13 | implemented, install checked for one skill | folders moved from `.claude/skills/` to the repository root, `agents/openai.yaml` added to each; no `SKILL.md` changed; `npx skills add --list` found all three and a single-skill install delivered every file of the illustration skill |
| Illustration pipeline | FD-D3, FD-D4, FD-D5 | implemented | `render.py` output pixel-identical to a hand-made set for two source pages, light and dark |
| Existing-landing check | FD-D6 | implemented, trial did not separate the two runs | both runs on an app repository stopped without writing a file |
| Landing page floor | FD-D7 | implemented, one rule broken in the trial and fixed | see FD-D12 |
| Verification scripts | FD-D8 | implemented | `shoot.py` and `lighthouse.py` run on two real pages and one broken page |
| Unattended runs | FD-D9 | implemented | `questions.md` written by every trial run |
| Repository and skill names | FD-D14 | implemented, install checked for all three | `npx skills add --list` found all three on the published repository and a global install of all three succeeded for Claude Code and Gemini CLI |
| Optional hand-off to the render skill | FD-D16 | implemented, fallback not run | `quick_validate` passes on the edited `frontdoor-readme` |
| Signature per repository, no shipped look | FD-D17, FD-D21, FD-D22 | implemented, trial on two greenfield repositories | see Phase 5 |
| Hero banner in every run | FD-D18 | implemented, greenfield trialled, brownfield not | see Phase 5 |
| Complete README with traced facts | FD-D19 | implemented, trialled twice | see Phase 5 |
| Scene first, diagram where it fits, `<details>` | FD-D20 | implemented | `frontdoor-readme` guidance rewritten; this repository's README follows it |
| Local board for rough directions | FD-D24, FD-D31 | implemented, Windows only, no skill run end to end | see Phase 6 and Phase 7 |
| Banner, still social preview, optional animated banner | FD-D32, FD-D33 | implemented, animated WebP only, Windows only, no skill run end to end | see Phase 7 and Phase 8 |
| Animation render speed | FD-D34, FD-D35 | implemented, script run on two real pages, uncommitted | see Phase 9 |
| Host selection | FD-Q1 | unobserved, descriptions changed since | no run started from a plain request |
| Automated tests | FD-Q2 | started for `fd` only | `tests/`, 43 pass; the other scripts have none |
| Other operating systems | FD-Q3 | unobserved | Windows and Edge only |
| UI gallery skill | UG-D1 to UG-D10, pack `ui-gallery` | implemented, run on three apps | roadmap of the `ui-gallery` pack |
| `frontdoor-core` and the harness `fd` | FD-D36, FD-D40, FD-D41 | implemented, uncommitted, Windows only | see Phase 10 |
| Board v2 | FD-D37, FD-D38, FD-D39 | planned | Phase 11 |
| The three skills on the core, variant count asked | FD-D36, FD-D40 | planned | Phase 12 |
| Local board server | FD-D39 | planned | Phase 13 |
| Project-scope skills for writing the harness | FD-D42 | installed, git-ignored | `uv`, `ruff`, `python-testing-patterns`, `create-cli` copied into `.kiro/skills/` and `.claude/skills/`; `git status` lists none of them |

## Phase 1: build the three skills

Acceptance criteria:

- each skill has a `SKILL.md` with frontmatter and an assertive description, under 500 lines
- every script a skill tells the agent to run exists in that skill's folder and runs
- no skill requires a file from another skill

### Checkpoint: complete

| Item | Result |
|---|---|
| Skills created | `frontdoor-readme`, `frontdoor-illustrate`, `frontdoor-landing` |
| Scripts | `render.py`, `shoot.py` (`check`, `og`), `lighthouse.py` |
| Validation | `quick_validate` passes for all three |
| Script runs | `render.py` against two source pages, light and dark, byte-compared as decoded pixels: no difference |
| Cross-skill references | optional only; checked by reading each `SKILL.md` |

## Phase 2: trial on two real repositories, with and without the skills

Acceptance criteria:

- three scenarios, each run once with the skills and once without, in disposable clones
- every run's outcome graded against stated assertions and compared by a person

### Checkpoint: complete

| Scenario | With skills | Without skills |
|---|---|---|
| README illustrations for an app repository, at most 6 | 8 of 8 assertions | 8 of 8 |
| Landing page for a skills repository with none | 10 of 11 | 11 of 11 |
| Landing page for an app repository that has a docs site | 5 of 5, stopped | 5 of 5, stopped |

- The single missed assertion was a skill count in a heading, recorded in FD-D12.
- A person compared the outputs side by side and preferred the with-skill result for both the landing page and the README illustrations, 2026-10-10.
- The pass rates do not separate the two sides; the comparison by a person is the evidence for the skills.
- Elapsed time and token counts are not comparable: both without-skills runs were interrupted and resumed, so their figures cover only the resumed part.
- The two with-skill runs also produced findings that changed the skills, listed in Phase 3.
- The review page built by the plugin was unusable; see FD-D11.

## Phase 3: revise the skills from the trial findings

Acceptance criteria:

- every finding a trial agent reported with a reproduction is fixed or recorded as open
- each changed script is run again

### Checkpoint: complete

| Item | Result |
|---|---|
| `lighthouse.py` added | ran on two pages, mobile and desktop |
| `shoot.py` | now scrolls before the reduced-motion shot, checks the preview file and its size, accepts `--axe` and `--schemes`; run on two real pages and one broken page |
| `render.py` | clear message for a page outside the root; quiet server; re-run on one page |
| Skill text | placement and Actions deploy, contributor rules, unattended runs, font preload, narrow-screen figures, brand conflicts, linter folders, ring and lane starter components |
| Not re-run | the three trial scenarios after the edits |

## Phase 5: a signature per repository, a hero in every run, a complete README

Acceptance criteria:

- no reusable look is shipped: the starter carries only the renderer contract and a placeholder marker
- `render.py` reports a requested font that did not load and a stylesheet that still carries the marker
- `frontdoor-readme` ends every run with a hero banner and writes a complete README with a fact trace
- two unlike greenfield repositories come out with different signatures, and neither is this repository's look

### Checkpoint: complete, with a second trial not run

| Item | Result |
|---|---|
| Starter and references | `starter.css` holds the contract only; `signature.md` copied byte-identical into the three skills (checked with `cmp`); `scene-craft.md`, `readme-content.md`, `contrast.py` added |
| `render.py` | on the untouched starter: WARN and exit 1; with a font name that does not exist: WARN and exit 1; on this repository's two source pages: exit 0 with the fonts printed |
| Validation | `quick_validate` passes for all three skills |
| Trial | two agents followed the skills on `driftcheck` (a command-line tool) and `pebble` (a children's story reader) with no user to answer; every image of the two sets and of this repository differs by hash |
| Signatures that came out | `driftcheck`: an audit desk with index cards, typewriter and slab faces, one vermilion stamp; `pebble`: a still pond with stones and ripples, Fraunces and Andika, teal |
| Fact trace | each README came with a source for every line; rows without a source were flagged and became questions (the audience sentence and the install path of `driftcheck`; the install command and the dev-server address of `pebble`) |
| Fixes from the trial | `render.py` names SVG elements, skips `data-bleed`, scans `svg text` for fonts; `signature.md` says six lines and uses unusual example subjects and lists overused typefaces; the sketch folder, the owner of the signature step, the `--root` meaning, a command that cannot work as written, a description that outruns the code and the metaphor rule are written into the skills |
| This repository | the four pictures that restate the skills were redrawn and the README text updated to match |
| Known gap | the box check of `render.py` sees the item only, so a label that runs out of its card passes; the skill says to look at every image |
| Not run | a second trial after the fixes; a brownfield run with an existing banner; the new steps of `frontdoor-landing` |
| Not observed | skills chosen from a plain request after the description changes (FD-Q1); the README on github.com |

## Phase 6: a local board for rough directions

Acceptance criteria:

- every round of rough directions lands on one local page per repository, not on a hosted page
- `board.py` is identical in the three skills and runs with the standard library only
- a bad input stops the script before it records anything

### Checkpoint: complete, no skill run end to end

| Item | Result |
|---|---|
| Script | `board.py` added to the three skills (`add`, `build`, `choose`, `--inline`, `--no-open`); copies compared with `cmp` |
| Text | "Show the directions" section added to `signature.md` (still three identical copies); the scratch-folder wording in the three `SKILL.md` files replaced by `.frontdoor/` and the board; `AGENTS.md` carries the rule |
| Runs | throwaway repository: two rounds, ids continued, a choice recorded, five bad inputs stopped with exit 1, `.gitignore` written; `ghist`: two rounds of three directions, board checked at 1200 px light and 400 px dark |
| Not run | a skill following the new text from a plain request; macOS and Linux; the board in Firefox and Safari |

## Phase 7: a board per purpose, banner and banner-social, an optional animated banner

Acceptance criteria:

- each purpose (readme, landing-page, product) has its own board folder and `board.py` refuses any other folder
- `frontdoor-readme` makes `banner` and `banner-social`, and `render.py` enforces GitHub's social preview rules on a `data-social` item; the social preview is always a still PNG holding only the brand name and the branding element
- a GIF README banner is offered with a brief of the motion and built only on approval

### Checkpoint: complete, no skill run end to end

| Item | Result |
|---|---|
| Board | `board.py` takes `.frontdoor/<purpose>`; on a throwaway repository `.frontdoor/readme` added a round and wrote `.gitignore`, `.frontdoor` and `.frontdoor/other` stopped with exit 1; the three copies of `board.py` and `signature.md` compared with `cmp` |
| Social preview | `render.py` on a test page: a `data-social` item wrote 1280x640 PNGs, and the one text element inside the 40 px border was reported by name |
| GIF | `scripts/animate.py` on the awsketch source page: 90 frames, 1.68 MB light and 1.85 MB dark, identical in size to the hand-made files; README banner only, the social preview is a still image |
| PNG chosen over JPG | awsketch social card at 1280x640: PNG 155 / 167 KB, JPG at quality 90 90 / 88 KB (light / dark); the user kept PNG |
| Text | `frontdoor-readme/references/banner.md` added; `SKILL.md` steps 3, 4 and 5, `github-readme.md`, `audit-and-plan.md`, `AGENTS.md` and the board paths in the other two skills edited |
| Not run | a skill following the new text from a plain request; the GIF and PNG on github.com; macOS and Linux |

## Phase 8: animated WebP only

Acceptance criteria:

- `scripts/animate.py` writes looping animated WebP, rounded and bordered, in a `sway` and a `loop` motion, and no GIF is written
- `frontdoor-readme` and `frontdoor-illustrate` name the script, and no skill text offers a GIF or a reduced-motion source for the banner

### Checkpoint: script run on a real page, no skill run end to end

| Item | Result |
|---|---|
| Script | `animate.py --motion loop` on the Docker Zero hero page: 30 frames, 2400x840, 672 KB light and 642 KB dark, exit 0 |
| Size comparison | same 30 frames: GIF 7.6 MB and WebP 650 KB at 2400x840; GIF 3.0 MB and WebP 306 KB at 1200x420 |
| Text | `banner.md`, `SKILL.md` of `frontdoor-readme` and of `frontdoor-illustrate`, `github-readme.md` and `AGENTS.md` edited |
| Not run | `--motion sway` end to end; the WebP on github.com; macOS and Linux |

## Phase 9: a faster `animate.py`

Acceptance criteria:

- every frame is encoded in a worker pool as soon as it is captured, and the script joins the animated WebP itself (FD-D35)
- the themes are captured in parallel, a repeated sway value is drawn once, and `--draft` and `--batch` exist
- the files are no larger and score the same PSNR as FD-D34's files on the same pages

### Checkpoint: script run on two real pages, no skill run end to end

| Item | Result |
|---|---|
| Loop | Skillmesh banner, 2400x880, 40 frames: 111 s and 706 / 728 KB before, 22 s and 311 / 324 KB after; PSNR 37.3 / 37.2 dB mean |
| Sway | Homeware hero, 2400x800, 30 frames, 15 drawn: 46 s and 321 / 255 KB before, 18 s and 188 / 143 KB after; PSNR 37.8 dB both |
| Batch | both banners in one run, one of them at `--size 1500x500`, and a job with a missing id: 25 s for the two pictures, the bad job reported by name, exit 1 |
| Draft | the Skillmesh banner: 600x220, 12 frames, loop 3333 ms like the real file, 12 s |
| Errors | a missing id stops in seconds with its name; a `--call` without `{v}` and a missing source exit with a message; no `.part` file left behind |
| Text | `animate.py` docstring and `banner.md` edited |
| Not run | macOS and Linux; a drawing that changes nearly every pixel each frame; the files on github.com |

## Phase 10: `frontdoor-core` and the harness `fd`

Depends on: none.

Acceptance criteria:

- a skill `frontdoor-core` at the repository root, invocable on its own, holds `signature.md`, the design board method, the render contract for items of any size, `animate.py` and the harness `fd` (FD-D36)
- `fd` offers `page add`, `round new --count N` with `--count` required (FD-D40), `round add` that pairs the light and dark renders by file name, `status --json`, `render` and `animate`
- a daemon keeps one browser open between commands, with `--watch` (FD-D41); still WebP encodes run in parallel, and the `method=4` file size is checked against `method=6` on several pages before it becomes the default
- a first pytest suite covers `fd`, with the real-browser tests behind a marker
- `AGENTS.md` states the new dependency rule and drops the `cmp` rule for the copies that no longer exist

### Checkpoint: complete, uncommitted, the three skills not yet on the core

| Item | Result |
|---|---|
| Skill | `frontdoor-core` added at the repository root: `SKILL.md`, `agents/openai.yaml`, references `signature.md` (its board section now points to `board.md`), `board.md`, `harness.md`, `source-page.md` (items of any size, `data-finish`), assets `board.html`, `starter.css`, `starter.html`, `shared.js`, scripts `fd.py` with the package `fdlib`, `animate.py`, `contrast.py`; `quick_validate` reports it valid |
| `fd` | `page add`/`list`, `round new` (`--count` required, 1 to 12), `round add`, `choose`, `status [--json]`, `board build`/`open`, `render [--watch]`, `animate`, `contrast`, `daemon start`/`stop`/`status`/`run` |
| Speed, same machine | `fd render` on `assets/source/readme.html` (10 items, 2 themes): 12.5 s against 40.7 s for `render.py`; on `scenes.html` 14.8 s against 48.3 s; with the daemon running a full page took 9.6 s and one item 3.6 s, against 5.7 s for one item without it |
| `method=4` | on the 20 pictures of the two pages: 1837 KB against 1839 KB at method 6, the largest file 1.7 percent larger, every file pixel-identical to the `render.py` output; 4 is the default |
| Tests | `tests/`: 43 pass with `--browser-tests` (board model, finishes, real renders, an id used twice, an unknown item, an overflow warning, an edited stylesheet seen by a long-lived browser, the daemon with a wrong token refused, `--watch`); no Edge process left after the run; `ruff check` clean |
| End to end | a throwaway repository: a page, a round of 2 variants, two renders, `round add` paired 4 pictures in both themes, `choose`, `status --json`; the board opened from `file://` loaded all 4 images, switched to dark and showed no console error |
| `AGENTS.md` | the core rule, the neutral look of frontdoor's own tooling, the board of `fd`, the `cmp` rule kept only until the move, and the test command |
| Not done here | the three skills still carry and use their own `signature.md`, `board.py`, `render.py` and `animate.py` (Phase 12), so no copy was deleted and the `cmp` rule stays; `board.html` is an interim shell (Phase 11) |
| Not run | macOS and Linux (FD-Q3); the daemon started from a host whose shell kills detached processes; a skill following the core's text from a plain request (FD-Q1) |

## Phase 11: board v2

Depends on: Phase 10.

Acceptance criteria:

- one board per repository under `.frontdoor/board/`, a page per use case with a free slug, rounds numbered per page and shown as tabs (FD-D37); a fixed shell page that reads its data from a script file, because a page opened from `file://` cannot fetch JSON
- the hover table of contents, one frame per image with the light/dark switch and the hover divider, the two-variant comparison off by default, the viewer for long images, deep links and keyboard movement between variants and rounds (FD-D38)
- a "Copy choice" button, and a data layout that holds choices and notes for the server of Phase 13 (FD-D39)
- the interface designed with `impeccable` and `design-taste-frontend`, then passed through their critique and audit
- tested on a copy of the `docker-zero` product board (`C:\.repos\Personal\kai\docker-zero\.frontdoor\product`, long portrait images) and on a page with many rounds

### Checkpoint: not started

## Phase 12: the three skills on the core, and two trial runs

Depends on: Phases 10 and 11.

Acceptance criteria:

- `frontdoor-readme`, `frontdoor-illustrate` and `frontdoor-landing` find the core beside them, stop when it is missing, and keep only their own steps (FD-D36)
- no skill text says "two or three"; every round asks the number of variants, and an unattended run makes 3 and records the question (FD-D40)
- one trial redesigns a component of a web page with `frontdoor-core` alone, and one trial runs `frontdoor-readme` end to end, each ending with its rounds on the board

### Checkpoint: not started

## Phase 13: local board server

Depends on: Phase 11.

Acceptance criteria:

- `fd board serve` serves the board on `127.0.0.1` with a token in the URL, records choices and per-variant notes into the board data, and reloads the board when a round is added (FD-D39)
- the agent reads the choice with `fd status --json` or waits for it with a command run in the background
- with the server stopped, the board still opens from `file://` and the copy button still works

### Checkpoint: not started

## Risks

| Risk | Detail |
|---|---|
| The three copies of `board.py` drift apart | FD-D24 |
| Descriptions may not trigger | FD-Q1 |
| A script regresses unnoticed | FD-Q2 |
| Another operating system fails at the first script | FD-Q3 |
| Lighthouse performance scores vary by 10 points or more between identical runs | FD-D8 |
| A generated page breaks a repository's own writing rules | FD-D12 |
| Examples or the typefaces of this repository's own look become the default of other repositories | FD-D17 |
| The three copies of `signature.md` drift apart | FD-D22; ends when FD-D36 leaves one copy in the core |
| A skill installed without `frontdoor-core` stops at its first step | FD-D36 |
| The board's look becomes a template for the pictures a repository gets | FD-D38 |

## Next action

Phase 11 next:

1. Start Phase 11: design board v2 with `impeccable` and `design-taste-frontend`, replacing the interim `frontdoor-core/assets/board.html` while keeping the data `fd` writes (pages, rounds, variants with paired light and dark pictures, choices, `compare`), and test it on a copy of the `docker-zero` product board.
2. Phase 10 left the three skills on their own copies; moving them onto the core is Phase 12.

Carried over from before Phase 10:

3. Run the trial again on two unlike greenfield repositories and on one brownfield repository with a banner, to check the fixes of Phase 5 and whether the first trial's examples still anchor the agents (FD-D23). Record the signatures and the image hashes.
4. Ask for a README upgrade and for a landing page in a plain sentence, in a repository that has the skills, and record whether each skill is selected (FD-Q1); the descriptions changed in Phase 5.
5. If a skill is not selected, run the description optimizer from the skill-creator plugin on it.
6. Decide whether the scripts need automated tests (FD-Q2) before anyone depends on them.
7. After the new text is installed from GitHub, ask for a hero in a plain sentence in a repository that has the skills and record whether the run builds a round under `.frontdoor/`, adds it to the board and opens it (FD-D24); run `board.py` once on macOS or Linux (FD-Q3).
8. Run `animate.py` once on a drawing that changes nearly every pixel each frame and compare its file size with the previous encoder (FD-D35); lower `--workers` and note the memory on a machine with little RAM.
9. Commit only when asked. The `animate.py` rewrite and its record are committed (`7b9a992`, `85f86cf`), and the plan for these phases is committed (`641ca53`); the Phase 10 work (`frontdoor-core/`, `tests/`, `AGENTS.md`) and its record here are uncommitted. The UI gallery skill's next actions are in the `ui-gallery` pack.
