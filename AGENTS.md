# Working in this repository

This repo is the source of the frontdoor skills. `npx skills add <repo> --skill <name>` installs a single skill folder, and nothing else travels with it.

| Path | Ships | Read by |
|---|---|---|
| `<skill>/SKILL.md`, `<skill>/agents/openai.yaml`, `<skill>/scripts/*`, `<skill>/assets/*`, `<skill>/references/*` | yes | the running agent |
| `AGENTS.md`, `README.md`, `docs/baseline/`, `tests/` | no | whoever works in this repo |
| `assets/` at the repository root: the README pictures, with their HTML sources in `assets/source/` | no | whoever reads or regenerates the README |

Each skill folder sits at the repository root. Do not move one under `.claude/skills/` or add a parent folder.

## Rules

- `frontdoor-core` holds what the skills share: the signature method, the design board, the render contract, the starter assets and the harness `fd` (`frontdoor-core/scripts/fd.py`, with `animate.py` and `contrast.py`). It runs alone and never reads a path outside its folder. `frontdoor-readme`, `frontdoor-illustrate` and `frontdoor-landing` require it: each finds it at `<skill-dir>/../frontdoor-core`, stops with a message to install `frontdoor-core` when it is missing, keeps only its own steps, and carries no copy of what the core holds. Apart from the core, a skill relies only on its own folder and names a sibling only as optional help. `frontdoor-ui-gallery` does not use the core.
- Ship no reusable look in what the skills make for a repository. A starter carries only the renderer contract; each repository gets its own signature of vector shape language, typeface and presentation, and this repository's own look is an example of one, not a template. Frontdoor's own tooling is not a product and keeps one neutral look everywhere: the page of `frontdoor-ui-gallery` and the design board of `frontdoor-core`.
- A hero banner named `banner` and a GitHub social preview named `banner-social` end every `frontdoor-readme` run, in a greenfield and in a brownfield repository. The social preview follows GitHub's rules, kept in `frontdoor-readme/references/banner.md`: 1280x640 px (at least 640x320), under 1 MB, a 40 pt safe border; `fd render` enforces them for an item marked `data-social`. The card carries only the brand name on the left and the branding element on the right, with no tagline, because a thumbnail in a chat app is too small to read one. GitHub accepts PNG, GIF or JPG, but the social preview is always a still PNG, never a GIF (chat and mail apps show no thumbnail for it) and not a JPG (PNG keeps thin lines and small text crisp, and it is already far under 1 MB).
- An animated README banner is optional, and only the README banner: `frontdoor-readme` suggests it, briefs the user on the motion and its costs, and builds it only after approval with `fd animate` (`frontdoor-core/scripts/animate.py`). The default is the still WebP. Animated WebP is the only animated format: never a GIF, and the README `<picture>` carries no `prefers-reduced-motion` source, so the banner moves for every reader.
- Rough directions are shown on the design board of the repository being worked on, never on a hosted page: `fd` keeps one board per repository in `.frontdoor/board/`, a page per use case with a free slug, each page numbering its own rounds, and asks for the number of variants every round (`--count` has no default). `.frontdoor/` is ignored by git and never committed.
- No step may need administrator rights. Scripts use the installed Edge or Chrome, run through `uvx ... python -I`, and write only where told.
- Skills write files and stop. They never commit or push, and neither do you unless asked.
- ASCII hyphen only, no en dash or em dash, in every file.
- Never hard-wrap a paragraph. One paragraph is one line.
- A `SKILL.md` is an instruction executed fresh on every run, in English and in the imperative. Give the reason only where a rule could be argued away.
- Do not state a skill count in prose; it goes stale when a skill is added or removed.

## Where reasoning goes

`docs/baseline/frontdoor/` is the decision log for the skills, and `docs/baseline/readme-design/` is the one for this repository's README pictures: scope, current truth, decisions with rejected alternatives, open questions, and the roadmap. Record the full argument there, not in a `SKILL.md`. Run `packtool check` on a pack after editing it if you have the tool.

## Changing a script

Re-run it on a real page before reporting it done: `frontdoor-landing/scripts/shoot.py check` and `lighthouse.py` on a landing page, and `frontdoor-ui-gallery/scripts/shoot.py render` and `check` on a repository that already has a `design/ui-gallery/gallery.json`.

The harness `fd` in `frontdoor-core/scripts/` has tests in `tests/`. Run `uvx --with pytest --with pillow --with playwright pytest tests -p no:cacheprovider --browser-tests` after changing it (without `--browser-tests` only the tests that need no browser run), then `fd render` on `assets/source/readme.html` and a round on a throwaway repository. Lint with `uvx ruff check --line-length 140 frontdoor-core/scripts tests`. The other scripts have no automated tests yet.
