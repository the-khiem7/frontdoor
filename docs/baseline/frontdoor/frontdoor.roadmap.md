---
baseline_schema: "2.0"
pack: "frontdoor"
document: "roadmap"
status: "active"
updated: "2026-10-11"
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
| Host selection | FD-Q1 | unobserved, descriptions changed since | no run started from a plain request |
| Automated tests | FD-Q2 | not started | none |
| Other operating systems | FD-Q3 | unobserved | Windows and Edge only |

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

## Risks

| Risk | Detail |
|---|---|
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
5. Commit only when asked.
