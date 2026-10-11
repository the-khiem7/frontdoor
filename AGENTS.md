# Working in this repository

This repo is the source of three skills. `npx skills add <repo> --skill <name>` installs a single skill folder, and nothing else travels with it.

| Path | Ships | Read by |
|---|---|---|
| `<skill>/SKILL.md`, `<skill>/agents/openai.yaml`, `<skill>/scripts/*`, `<skill>/assets/*`, `<skill>/references/*` | yes | the running agent |
| `AGENTS.md`, `README.md`, `docs/baseline/` | no | whoever works in this repo |
| `assets/` at the repository root: the README pictures, with their HTML sources in `assets/source/` | no | whoever reads or regenerates the README |

Each skill folder sits at the repository root. Do not move one under `.claude/skills/` or add a parent folder.

## Rules

- A skill must run alone. It may rely on anything inside its own folder (`scripts/`, `assets/`, `references/`). It may name a sibling skill as optional help, never as a prerequisite, and never reads a path outside its folder.
- Ship no reusable look. A starter carries only the renderer contract; each repository gets its own signature of vector shape language, typeface and presentation, and this repository's own look is an example of one, not a template.
- A hero banner ends every `frontdoor-readme` run, in a greenfield and in a brownfield repository.
- The `references/signature.md` copies in the three skills stay byte-identical: run `cmp` on `frontdoor-illustrate/references/signature.md` against each of the other two.
- No step may need administrator rights. Scripts use the installed Edge or Chrome, run through `uvx ... python -I`, and write only where told.
- Skills write files and stop. They never commit or push, and neither do you unless asked.
- ASCII hyphen only, no en dash or em dash, in every file.
- Never hard-wrap a paragraph. One paragraph is one line.
- A `SKILL.md` is an instruction executed fresh on every run, in English and in the imperative. Give the reason only where a rule could be argued away.
- Do not state a skill count in prose; it goes stale when a skill is added or removed.

## Where reasoning goes

`docs/baseline/frontdoor/` is the decision log for the skills, and `docs/baseline/readme-design/` is the one for this repository's README pictures: scope, current truth, decisions with rejected alternatives, open questions, and the roadmap. Record the full argument there, not in a `SKILL.md`. Run `packtool check` on a pack after editing it if you have the tool.

## Changing a script

Re-run it on a real page before reporting it done: `render.py` on a source page, `shoot.py check` and `lighthouse.py` on a landing page. No automated tests exist yet.
