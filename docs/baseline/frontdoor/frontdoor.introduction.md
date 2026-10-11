---
baseline_schema: "2.0"
pack: "frontdoor"
document: "introduction"
status: "active"
updated: "2026-10-11"
code_ref: "uncommitted"
---

# Frontdoor: Scope, Current Truth, Target

## Scope

Three Claude skills that raise how a repository presents itself, plus the scripts and references they carry.

| Skill | Job |
|---|---|
| `frontdoor-readme` | write or rewrite the complete README, with a hero banner and light/dark pictures made for that repository (FD-D18, FD-D19) |
| `frontdoor-illustrate` | turn hand-built HTML pages into rounded, bordered WebP images in a light and a dark theme |
| `frontdoor-landing` | design and build a single-file `index.html` for GitHub Pages, after checking that no landing page exists |

Out of scope: documentation other than the README, committing or pushing, enabling GitHub Pages (a repository setting the skills only describe), and any build step on the page being produced.

## Current truth

All three skills sit at the repository root as `<name>/` and are committed (FD-D13). Each passed `quick_validate` from the skill-creator plugin before it moved from `.claude/skills/`; the move changed no `SKILL.md`, and `quick_validate` was not re-run at the new path. `frontdoor-readme/SKILL.md` step 4 and `description` were reworded afterwards (FD-D16); `quick_validate` passes on that skill.

| Skill | Files |
|---|---|
| `frontdoor-readme` | `SKILL.md`; `agents/openai.yaml`; `references/github-readme.md`, `references/audit-and-plan.md`, `references/readme-content.md`, `references/signature.md` |
| `frontdoor-illustrate` | `SKILL.md`; `agents/openai.yaml`; `scripts/render.py`, `scripts/contrast.py`; `assets/starter.css`, `assets/starter.html`, `assets/shared.js`; `references/source-page.md`, `references/scene-craft.md`, `references/signature.md` |
| `frontdoor-landing` | `SKILL.md`; `agents/openai.yaml`; `scripts/shoot.py`, `scripts/lighthouse.py`; `references/existing-landing.md`, `references/pages-setup.md`, `references/page-craft.md`, `references/verify.md`, `references/signature.md` |

The pictures in this repository's own README are tracked in the `readme-design` pack (FD-D15 moved there).

Observed running, 2026-10-10, on Windows with Edge:

- `render.py` produced WebP files pixel-identical to a hand-made set for two different source pages.
- `shoot.py check` reported 0 FAIL on two real landing pages and 7 FAIL on a deliberately broken page, with the broken image, anchor, contrast and missing-metadata cases each reported.
- `lighthouse.py` returned the four category scores for two landing pages, mobile and desktop.
- A trial on two real repositories, each run with and without the skills, is recorded in the roadmap under Phase 2. The reviewer preferred the with-skill output for both the landing page and the README illustrations.
- 2026-10-12: two agents followed `frontdoor-readme` and `frontdoor-illustrate` on two invented greenfield repositories with unlike subjects; each produced a hero, a scene or flow, a README with a fact trace, and a different signature (roadmap Phase 5).

Not observed: installing `frontdoor-readme` or `frontdoor-landing` with `npx skills add`, the skills selected by a host from a plain request, any run on macOS or Linux, any page on its live GitHub Pages URL.

## Target

A person installs a skill with `npx skills add <repository> --skill <name>` and asks for a README upgrade or a landing page. The skills read that repository's brand, rules and tooling, then produce work that fits it, with no change to the skills.

## Constraints

| Constraint | Why |
|---|---|
| Each skill is self-contained: it runs its own scripts and names the others only as optional help | a skill installed alone must not point at a folder that is not there |
| No look is shipped: the starter carries only the renderer contract, and each repository gets its own signature of shape language, typeface and presentation (FD-D17) | each brand has its own identity, and a shipped look would make every repository look alike with only the text changed |
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
