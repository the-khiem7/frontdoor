# doorway

Claude skills that raise how a repository presents itself: a README built around pictures, illustrations rendered from HTML into light and dark pairs, and a single-file landing page for GitHub Pages.

## Skills

| Skill | Use it when | Result |
|---|---|---|
| `readme-visualization` | the README is a wall of text, ASCII diagrams or Mermaid | an audited plan, then a README that uses `<picture>` light/dark image pairs |
| `illustration-render` | you need pictures that match a brand and regenerate from text | rounded, bordered WebP files, one light and one dark per HTML block |
| `landing-pager` | the repository has no landing page and should have one | a single `index.html` with Open Graph preview, checked at three widths in both themes |

Each skill carries its own scripts and references. Install one folder and it works alone. Skills name each other only as optional help.

## Install

Install every skill, or one by name:

```bash
npx skills add https://github.com/<owner>/doorway.git
npx skills add https://github.com/<owner>/doorway.git --skill landing-pager
```

Then ask in a plain sentence, for example "make the README nicer to read" or "add a GitHub Pages landing page".

## Requirements

- `uv` and `uvx` to run the scripts (`uvx --from playwright --with pillow python -I ...`).
- Microsoft Edge or Google Chrome already installed. Nothing is downloaded and no administrator rights are needed.
- Node.js with `npx` for the Lighthouse run in `landing-pager`.

## Behaviour to know

- The skills write files and stop. They never commit or push.
- `landing-pager` stops and shows its evidence when it finds an existing landing page, and asks where `index.html` should go before writing.
- No look is fixed. The brand comes from the target repository; the starter colours and fonts are placeholders.
- Where nobody can answer a question, a skill takes the recommended default and writes the question and the assumed answer to `questions.md`.

## Status

Built and exercised on Windows with Edge. A trial on two real repositories, run with and without the skills, was preferred by a person for both the landing page and the README illustrations. Not yet observed: selection from a plain request, macOS or Linux, a page on its live GitHub Pages URL.

Scope, decisions and open questions live in [docs/baseline/visual-skills/](docs/baseline/visual-skills/).
