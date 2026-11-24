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
| Automated tests | FD-Q2 | not started | none |
| Other operating systems | FD-Q3 | unobserved | Windows and Edge only |
| UI gallery skill | UG-D1 to UG-D10, pack `ui-gallery` | implemented, run on three apps | roadmap of the `ui-gallery` pack |

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
| The three copies of `signature.md` drift apart | FD-D22 |

## Next action

1. Run the trial again on two unlike greenfield repositories and on one brownfield repository with a banner, to check the fixes of Phase 5 and whether the first trial's examples still anchor the agents (FD-D23). Record the signatures and the image hashes.
2. Ask for a README upgrade and for a landing page in a plain sentence, in a repository that has the skills, and record whether each skill is selected (FD-Q1); the descriptions changed in Phase 5.
3. If a skill is not selected, run the description optimizer from the skill-creator plugin on it.
4. Decide whether the scripts need automated tests (FD-Q2) before anyone depends on them.
5. After the new text is installed from GitHub, ask for a hero in a plain sentence in a repository that has the skills and record whether the run builds a round under `.frontdoor/`, adds it to the board and opens it (FD-D24); run `board.py` once on macOS or Linux (FD-Q3).
6. Run `animate.py` once on a drawing that changes nearly every pixel each frame and compare its file size with the previous encoder (FD-D35); lower `--workers` and note the memory on a machine with little RAM.
7. Commit only when asked; the `animate.py` rewrite, `banner.md` and this pack are uncommitted. The UI gallery skill's next actions are in the `ui-gallery` pack.
