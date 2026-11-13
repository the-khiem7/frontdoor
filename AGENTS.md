# Working in this repository

This repo is the source of the frontdoor skills. `npx skills add <repo> --skill <name>` installs a single skill folder, and nothing else travels with it.

| Path | Ships | Read by |
|---|---|---|
| `<skill>/SKILL.md`, `<skill>/agents/openai.yaml`, `<skill>/scripts/*`, `<skill>/assets/*`, `<skill>/references/*` | yes | the running agent |
| `AGENTS.md`, `README.md`, `docs/baseline/` | no | whoever works in this repo |
| `assets/` at the repository root: the README pictures, with their HTML sources in `assets/source/` | no | whoever reads or regenerates the README |

Each skill folder sits at the repository root. Do not move one under `.claude/skills/` or add a parent folder.

## Rules

- A skill must run alone. It may rely on anything inside its own folder (`scripts/`, `assets/`, `references/`). It may name a sibling skill as optional help, never as a prerequisite, and never reads a path outside its folder.
- Ship no reusable look. A starter carries only the renderer contract; each repository gets its own signature of vector shape language, typeface and presentation, and this repository's own look is an example of one, not a template. The one exception is the page of `frontdoor-ui-gallery`, a working tool for the people building an app, which keeps one neutral look.
- A hero banner named `banner` and a GitHub social preview named `banner-social` end every `frontdoor-readme` run, in a greenfield and in a brownfield repository. The social preview follows GitHub's rules, kept in `frontdoor-readme/references/banner.md`: 1280x640 px (at least 640x320), under 1 MB, a 40 pt safe border; `render.py` enforces them for an item marked `data-social`. The card carries only the brand name on the left and the branding element on the right, with no tagline, because a thumbnail in a chat app is too small to read one. GitHub accepts PNG, GIF or JPG, but the social preview is always a still PNG, never a GIF (chat and mail apps show no thumbnail for it) and not a JPG (PNG keeps thin lines and small text crisp, and it is already far under 1 MB).
- An animated GIF README banner is optional, and only the README banner: `frontdoor-readme` suggests it, briefs the user on the motion and its costs, and builds it only after approval. The default is the still WebP.
- The `references/signature.md` copies in `frontdoor-illustrate`, `frontdoor-readme` and `frontdoor-landing` stay byte-identical: run `cmp` on `frontdoor-illustrate/references/signature.md` against each of the other two. The `scripts/board.py` copies do the same, compared against `frontdoor-illustrate/scripts/board.py`.
- Rough directions are shown on a local board of the repository being worked on, one board per purpose in its own folder: `.frontdoor/readme/`, `.frontdoor/landing-page/` and `.frontdoor/product/`, each with its own `directions.html`, every round of one purpose on the same board, never on a hosted page. `board.py` refuses any other folder. `.frontdoor/` is ignored by git and never committed.
- No step may need administrator rights. Scripts use the installed Edge or Chrome, run through `uvx ... python -I`, and write only where told.
- Skills write files and stop. They never commit or push, and neither do you unless asked.
- ASCII hyphen only, no en dash or em dash, in every file.
- Never hard-wrap a paragraph. One paragraph is one line.
- A `SKILL.md` is an instruction executed fresh on every run, in English and in the imperative. Give the reason only where a rule could be argued away.
- Do not state a skill count in prose; it goes stale when a skill is added or removed.

## Where reasoning goes

`docs/baseline/frontdoor/` is the decision log for the skills, and `docs/baseline/readme-design/` is the one for this repository's README pictures: scope, current truth, decisions with rejected alternatives, open questions, and the roadmap. Record the full argument there, not in a `SKILL.md`. Run `packtool check` on a pack after editing it if you have the tool.

## Changing a script

Re-run it on a real page before reporting it done: `render.py` on a source page, `shoot.py check` and `lighthouse.py` on a landing page, `board.py` on a throwaway repository with two rounds, a missing file, an id used twice and `--inline`, and `frontdoor-ui-gallery/scripts/shoot.py render` and `check` on a repository that already has a `design/ui-gallery/gallery.json`. No automated tests exist yet.
