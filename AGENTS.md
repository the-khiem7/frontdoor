# Working in this repository

This repo is the source of three skills. `npx skills add <repo> --skill <name>` installs a single skill folder, and nothing else travels with it.

| Path | Ships | Read by |
|---|---|---|
| `<skill>/SKILL.md`, `<skill>/agents/openai.yaml`, `<skill>/scripts/*`, `<skill>/assets/*`, `<skill>/references/*` | yes | the running agent |
| `AGENTS.md`, `README.md`, `docs/baseline/` | no | whoever works in this repo |

Each skill folder sits at the repository root. Do not move one under `.claude/skills/` or add a parent folder.

## Rules

- A skill must run alone. It may rely on anything inside its own folder (`scripts/`, `assets/`, `references/`). It may name a sibling skill as optional help, never as a prerequisite, and never reads a path outside its folder.
- Fix no visual style. Starter colours and fonts are placeholders; the brand comes from the repository the skill runs in.
- No step may need administrator rights. Scripts use the installed Edge or Chrome, run through `uvx ... python -I`, and write only where told.
- Skills write files and stop. They never commit or push, and neither do you unless asked.
- ASCII hyphen only, no en dash or em dash, in every file.
- Never hard-wrap a paragraph. One paragraph is one line.
- A `SKILL.md` is an instruction executed fresh on every run, in English and in the imperative. Give the reason only where a rule could be argued away.
- Do not state a skill count in prose; it goes stale when a skill is added or removed.

## Where reasoning goes

`docs/baseline/visual-skills/` is the decision log: scope, current truth, decisions with rejected alternatives, open questions, and the roadmap. Record the full argument there, not in a `SKILL.md`. Run `packtool check` on the pack after editing it if you have the tool.

## Changing a script

Re-run it on a real page before reporting it done: `render.py` on a source page, `shoot.py check` and `lighthouse.py` on a landing page. No automated tests exist yet.
