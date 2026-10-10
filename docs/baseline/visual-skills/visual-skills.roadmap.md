---
baseline_schema: "2.0"
pack: "visual-skills"
document: "roadmap"
status: "active"
updated: "2026-10-11"
code_ref: "uncommitted"
---

# Visual Skills Roadmap

Reasoning for every row below lives in `visual-skills.hallucination.md` under the entry named in its Basis column. Do not restate it here.

## Status by area

| Area | Basis | Status | Evidence |
|---|---|---|---|
| Three skills and their split | VS-D1, VS-D2 | implemented | `quick_validate` reported each valid before the move in the next row |
| Layout for `npx skills add` | VS-D13 | implemented, install checked for one skill | folders moved from `.claude/skills/` to the repository root, `agents/openai.yaml` added to each; no `SKILL.md` changed; `npx skills add --list` found all three and a single-skill install delivered every file of `doorway-illustrate` |
| Illustration pipeline | VS-D3, VS-D4, VS-D5 | implemented | `render.py` output pixel-identical to a hand-made set for two source pages, light and dark |
| Existing-landing check | VS-D6 | implemented, trial did not separate the two runs | both runs on an app repository stopped without writing a file |
| Landing page floor | VS-D7 | implemented, one rule broken in the trial and fixed | see VS-D12 |
| Verification scripts | VS-D8 | implemented | `shoot.py` and `lighthouse.py` run on two real pages and one broken page |
| Unattended runs | VS-D9 | implemented | `questions.md` written by every trial run |
| Skill names carry the brand | VS-D14 | implemented | folders, `name` frontmatter, `openai.yaml` and README renamed; `npx skills add --list` not re-run under the new names |
| Host selection | VS-Q1 | unobserved | no run started from a plain request |
| Automated tests | VS-Q2 | not started | none |
| Other operating systems | VS-Q3 | unobserved | Windows and Edge only |

## Phase 1: build the three skills

Acceptance criteria:

- each skill has a `SKILL.md` with frontmatter and an assertive description, under 500 lines
- every script a skill tells the agent to run exists in that skill's folder and runs
- no skill requires a file from another skill

### Checkpoint: complete

| Item | Result |
|---|---|
| Skills created | `doorway-readme`, `doorway-illustrate`, `doorway-landing` |
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

- The single missed assertion was a skill count in a heading, recorded in VS-D12.
- A person compared the outputs side by side and preferred the with-skill result for both the landing page and the README illustrations, 2026-10-10.
- The pass rates do not separate the two sides; the comparison by a person is the evidence for the skills.
- Elapsed time and token counts are not comparable: both without-skills runs were interrupted and resumed, so their figures cover only the resumed part.
- The two with-skill runs also produced findings that changed the skills, listed in Phase 3.
- The review page built by the plugin was unusable; see VS-D11.

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

## Risks

| Risk | Detail |
|---|---|
| Descriptions may not trigger | VS-Q1 |
| A script regresses unnoticed | VS-Q2 |
| Another operating system fails at the first script | VS-Q3 |
| Lighthouse performance scores vary by 10 points or more between identical runs | VS-D8 |
| A generated page breaks a repository's own writing rules | VS-D12 |

## Next action

1. Run `npx skills add <repository> --skill <name>` into a scratch repository for `doorway-readme` and `doorway-landing`, and record whether each folder installs whole, scripts and references included (VS-D13).
2. Ask for a README upgrade and for a landing page in a plain sentence, in a repository that has the skills, and record whether each skill is selected (VS-Q1).
3. If a skill is not selected, run the description optimizer from the skill-creator plugin on it.
4. Decide whether the three scripts need automated tests (VS-Q2) before anyone depends on them.
5. Nothing in this pack waits on another decision.
