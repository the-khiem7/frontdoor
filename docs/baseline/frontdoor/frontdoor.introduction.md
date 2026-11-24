---
baseline_schema: "2.0"
pack: "frontdoor"
document: "introduction"
status: "active"
updated: "2026-11-24"
code_ref: "uncommitted"
---

# Frontdoor: Scope, Current Truth, Target

## Scope

Claude skills that raise how a repository presents itself, and how its app's UI can be reviewed, plus the scripts and references they carry.

| Skill | Job |
|---|---|
| `frontdoor-readme` | write or rewrite the complete README, with a hero banner and light/dark pictures made for that repository (FD-D18, FD-D19) |
| `frontdoor-illustrate` | turn hand-built HTML pages into rounded, bordered WebP images in a light and a dark theme |
| `frontdoor-landing` | design and build a single-file `index.html` for GitHub Pages, after checking that no landing page exists |
| `frontdoor-ui-gallery` | render every view and state of an app's UI from its real frontend with the backend mocked, in light and dark, on one review page (UG-D1 in the `ui-gallery` pack) |
| `frontdoor-core` (Phases 10 and 11; the other skills not yet moved onto it) | the shared core the other skills will require: the signature method, the design board and its harness `fd`, the render contract for items of any size; invocable on its own for design work no other skill covers (FD-D36) |

Out of scope: documentation other than the README, committing or pushing, enabling GitHub Pages (a repository setting the skills only describe), and any build step on the page being produced.

## Current truth

Every skill sits at the repository root as `<name>/` (FD-D13); `frontdoor-ui-gallery` is the newest and passes `quick_validate`. Each passed `quick_validate` from the skill-creator plugin before it moved from `.claude/skills/`; the move changed no `SKILL.md`, and `quick_validate` was not re-run at the new path. `frontdoor-readme/SKILL.md` step 4 and `description` were reworded afterwards (FD-D16); `quick_validate` passes on that skill.

| Skill | Files |
|---|---|
| `frontdoor-readme` | `SKILL.md`; `agents/openai.yaml`; `scripts/animate.py`, `scripts/board.py`; `references/github-readme.md`, `references/audit-and-plan.md`, `references/readme-content.md`, `references/banner.md`, `references/signature.md` |
| `frontdoor-illustrate` | `SKILL.md`; `agents/openai.yaml`; `scripts/render.py`, `scripts/contrast.py`, `scripts/board.py`; `assets/starter.css`, `assets/starter.html`, `assets/shared.js`; `references/source-page.md`, `references/scene-craft.md`, `references/signature.md` |
| `frontdoor-landing` | `SKILL.md`; `agents/openai.yaml`; `scripts/shoot.py`, `scripts/lighthouse.py`, `scripts/board.py`; `references/existing-landing.md`, `references/pages-setup.md`, `references/page-craft.md`, `references/verify.md`, `references/signature.md` |
| `frontdoor-ui-gallery` | `SKILL.md`; `agents/openai.yaml`; `scripts/shoot.py`, `scripts/real.ps1`; `assets/gallery.html`, `assets/mock-kit.ts`, `assets/fixtures.ts`, `assets/vite.gallery.ts`; `references/states.md`, `references/manifest.md`, `references/real-capture.md`, `references/stacks/index.md`, `wails3.md`, `tauri2.md`, `svelte.md`, `vue.md` |
| `frontdoor-core` | `SKILL.md`; `agents/openai.yaml`; `scripts/fd.py` with the package `scripts/fdlib/`, `scripts/animate.py`, `scripts/contrast.py`; `assets/board.html`, `assets/starter.css`, `assets/starter.html`, `assets/shared.js`; `references/signature.md`, `references/board.md`, `references/harness.md`, `references/source-page.md` |

`tests/` at the repository root holds the pytest suite of `fd`; it does not ship.

The pictures in this repository's own README are tracked in the `readme-design` pack (FD-D15 moved there).

Observed running, 2026-10-10, on Windows with Edge:

- `render.py` produced WebP files pixel-identical to a hand-made set for two different source pages.
- `shoot.py check` reported 0 FAIL on two real landing pages and 7 FAIL on a deliberately broken page, with the broken image, anchor, contrast and missing-metadata cases each reported.
- `lighthouse.py` returned the four category scores for two landing pages, mobile and desktop.
- A trial on two real repositories, each run with and without the skills, is recorded in the roadmap under Phase 2. The reviewer preferred the with-skill output for both the landing page and the README illustrations.
- 2026-10-12: two agents followed `frontdoor-readme` and `frontdoor-illustrate` on two invented greenfield repositories with unlike subjects; each produced a hero, a scene or flow, a README with a fact trace, and a different signature (roadmap Phase 5).
- 2026-10-12: `board.py` put two rounds of rough directions for `ghist` on one local board, `.frontdoor/directions.html`, replacing the scratch folder outside the repository (FD-D24).
- 2026-10-22: `frontdoor-ui-gallery` built galleries for three desktop apps, two of them by a fresh agent given only the skill folder (pack `ui-gallery`).
- 2026-11-24: `animate.py` rendered two real banners, a `loop` and a `sway`, in 22 s and 18 s, at the same PSNR as the previous encoder and about half its file size; `--draft` and `--batch` ran on the same pages (roadmap Phase 9, FD-D35).
- 2026-11-24: `fd render` from `frontdoor-core` rendered this repository's two source pages pixel-identical to `render.py` in about a third of the time; the `fd` test suite passed, 43 tests with a real browser (roadmap Phase 10).

Not observed: installing `frontdoor-readme` or `frontdoor-landing` with `npx skills add`, the skills selected by a host from a plain request, any run on macOS or Linux, any page on its live GitHub Pages URL.

## Target

A person installs a skill with `npx skills add <repository> --skill <name>` and asks for a README upgrade or a landing page. The skills read that repository's brand, rules and tooling, then produce work that fits it, with no change to the skills.

After Phases 10 to 12, the person installs `frontdoor-core` beside any other frontdoor skill, and can also invoke the core alone for design work outside the README, the landing page and the product pictures, such as redesigning one component of a web page (FD-D36). Every design round of a repository lands on one board, split into a page per use case with its own round numbers (FD-D37), asks how many variants to make (FD-D40), and shows each image in one frame with a light/dark switch and divider (FD-D38). Repeated work goes through the harness `fd`, which keeps a browser open between commands (FD-D41).

## Constraints

| Constraint | Why |
|---|---|
| Each skill is self-contained: it runs its own scripts and names the others only as optional help | a skill installed alone must not point at a folder that is not there; replaced in Phase 10 by a required `frontdoor-core` beside each skill (FD-D36) |
| No look is shipped: the starter carries only the renderer contract, and each repository gets its own signature of shape language, typeface and presentation (FD-D17); the gallery page of `frontdoor-ui-gallery` is the one exception (UG-D2 in the `ui-gallery` pack), and the design board, as part of the harness, is the second (FD-D38) | each brand has its own identity, and a shipped look would make every repository look alike with only the text changed |
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
