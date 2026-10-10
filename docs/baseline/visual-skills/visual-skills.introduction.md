---
baseline_schema: "2.0"
pack: "visual-skills"
document: "introduction"
status: "active"
updated: "2026-10-11"
code_ref: "2e60fdc"
---

# Visual Skills: Scope, Current Truth, Target

## Scope

Three Claude skills that raise how a repository presents itself, plus the scripts and references they carry.

| Skill | Job |
|---|---|
| `readme-visualization` | audit a README, plan which sections become pictures, rewrite the page with light/dark image pairs |
| `illustration-render` | turn hand-built HTML pages into rounded, bordered WebP images in a light and a dark theme |
| `landing-pager` | design and build a single-file `index.html` for GitHub Pages, after checking that no landing page exists |

Out of scope: writing the project's own documentation, committing or pushing, enabling GitHub Pages (a repository setting the skills only describe), and any build step on the page being produced.

## Current truth

All three skills sit at the repository root as `<name>/` and are committed (VS-D13). Each passed `quick_validate` from the skill-creator plugin before it moved from `.claude/skills/`; the move changed no `SKILL.md`, and `quick_validate` was not re-run at the new path.

| Skill | Files |
|---|---|
| `readme-visualization` | `SKILL.md`; `agents/openai.yaml`; `references/github-readme.md`, `references/audit-and-plan.md` |
| `illustration-render` | `SKILL.md`; `agents/openai.yaml`; `scripts/render.py`; `assets/starter.css`, `assets/starter.html`, `assets/shared.js`; `references/source-page.md` |
| `landing-pager` | `SKILL.md`; `agents/openai.yaml`; `scripts/shoot.py`, `scripts/lighthouse.py`; `references/existing-landing.md`, `references/pages-setup.md`, `references/page-craft.md`, `references/verify.md` |

Observed running, 2026-10-10, on Windows with Edge:

- `render.py` produced WebP files pixel-identical to a hand-made set for two different source pages.
- `shoot.py check` reported 0 FAIL on two real landing pages and 7 FAIL on a deliberately broken page, with the broken image, anchor, contrast and missing-metadata cases each reported.
- `lighthouse.py` returned the four category scores for two landing pages, mobile and desktop.
- A trial on two real repositories, each run with and without the skills, is recorded in the roadmap under Phase 2. The reviewer preferred the with-skill output for both the landing page and the README illustrations.

Not observed: installing `readme-visualization` or `landing-pager` with `npx skills add`, the skills selected by a host from a plain request, any run on macOS or Linux, any page on its live GitHub Pages URL.

## Target

A person installs a skill with `npx skills add <repository> --skill <name>` and asks for a README upgrade or a landing page. The skills read that repository's brand, rules and tooling, then produce work that fits it, with no change to the skills.

## Constraints

| Constraint | Why |
|---|---|
| Each skill is self-contained: it runs its own scripts and names the others only as optional help | a skill installed alone must not point at a folder that is not there |
| No look is fixed; the starter tokens are placeholders and the brand comes from the target repository | each brand has its own identity, and a fixed palette would make every repository look alike |
| No step needs administrator rights: scripts use the Edge or Chrome already installed and write only where told | the machine these skills run on is a standard user account |
| The skills write files and stop; they never commit or push | a commit or a push is the user's decision |
| ASCII hyphen only in every file | a dash check may scan the files |
| Skill text is English, in the imperative, with the reason given where a rule could be argued away | the skills are read fresh on every run |

## Platform facts the skills rely on

None of these was checked on github.com from here; they come from the platform's documented behaviour and from what the trial runs showed.

- A GitHub README keeps `<picture>`, `<details>`, tables and relative images, and drops CSS, JavaScript and iframes. An SVG loaded through `<img>` does not load web fonts. There is no image map, so a row of image buttons is one image per link.
- GitHub Pages serves a branch from the root or `/docs`, or an Actions artifact; a project site lives under `/<repo>/`.
- Playwright can drive an installed Edge or Chrome through its channel option, so no browser download is needed.
- Lighthouse run through `npx` needs a browser that is already listening on a debugging port; its own launch of Edge failed in the trial.
