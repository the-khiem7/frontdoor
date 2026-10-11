<h1 align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.webp"><img src="assets/hero.webp" alt="frontdoor - Claude skills that raise how a repository presents itself. An arched door stands ajar and warm light spills out of it. Labels: README, illustrations, landing page." width="100%"></picture></h1>

**Claude skills that raise how a repository presents itself: a README built around pictures, illustrations rendered from HTML into light and dark pairs, and a single-file landing page for GitHub Pages.**

## Skills

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/skills-map-dark.webp"><img src="assets/skills-map.webp" alt="Map of the skills, each an arched card. frontdoor-readme: in, no README, or a wall of text, ASCII diagrams or Mermaid; out, a complete README with a hero banner and light and dark pictures. frontdoor-illustrate: in, pictures with a look of their own, regenerated from text; out, rounded, bordered WebP, one light and one dark per HTML block. frontdoor-landing: in, a repository with no landing page; out, one index.html with an Open Graph preview. Dashed arrows labelled optional help run from frontdoor-readme and from frontdoor-landing to frontdoor-illustrate. Each skill carries its own scripts and references; install one folder and it works alone." width="100%"></picture>

| Skill | Use it when | Result |
|---|---|---|
| `frontdoor-readme` | the README is missing, or a wall of text, ASCII diagrams or Mermaid | a complete README with a hero banner and `<picture>` light/dark image pairs, in a look drawn from your repository |
| `frontdoor-illustrate` | you need pictures with a look of their own that regenerate from text | rounded, bordered WebP files, one light and one dark per HTML block |
| `frontdoor-landing` | the repository has no landing page and should have one | a single `index.html` with Open Graph preview, checked at three widths in both themes |

Each skill carries its own scripts and references. Install one folder and it works alone. Skills name each other only as optional help.

## How each skill runs

### frontdoor-readme

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/scene-readme-dark.webp"><img src="assets/scene-readme.webp" alt="Illustration for frontdoor-readme: a wall of text becomes picture pairs. On the left, a pile of pages packed with lines of text and an ASCII box diagram, labelled a wall of text. Small pages travel along dotted lines to an arched blue door that stands ajar with warm light, labelled audited plan. On the right is the result: a README page with a banner, a light and dark picture pair, small figures and a light and dark toggle, labelled picture pairs." width="100%"></picture>

It plans before it builds: nothing is rewritten until the plan is approved.

<details>
<summary>Step by step</summary>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/readme-flow-dark.webp"><img src="assets/readme-flow.webp" alt="Flow of frontdoor-readme, in order. 1 Classify: read the code, the docs and any README, and decide greenfield or brownfield. 2 Facts and questions: a fact list with a source for each line, and labelled questions for the rest. 3 Signature and hero: a look drawn from this project, and a hero banner in every run. 4 Plan: the section order, scenes and diagrams, the hero and the files to add. Then wait for approval, because a README is the page every visitor sees. 5 Build: images from frontdoor-illustrate when it is available, otherwise ask how. 6 Write: the complete README, every sentence and command traced to the repository. 7 Verify: tests when there are any, image paths, anchors, and the trace of each statement. 8 Record: the work is left in the working tree and never committed, and the skill offers to log the decision." width="100%"></picture>

</details>

### frontdoor-illustrate

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/scene-illustrate-dark.webp"><img src="assets/scene-illustrate.webp" alt="Illustration for frontdoor-illustrate: one HTML block becomes one light and one dark picture. On the left, a code window holding an HTML block, labelled HTML block. In the middle, a camera labelled render.py. On the right, two rounded, bordered pictures: a light one with a sun and an arched door, and a dark one with a moon and the same door." width="100%"></picture>

Every image is an HTML block, so a later edit is a text edit plus one command.

<details>
<summary>Step by step</summary>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/illustrate-flow-dark.webp"><img src="assets/illustrate-flow.webp" alt="Flow of frontdoor-illustrate, in order. 1 Find the brand: logo, CSS and docs; a signature already there is continued. 2 Find the signature: subject, metaphor, shapes and typeface, with rough directions for a new repository. 3 Pick a folder: copy the starter where no linter or docs site looks. 4 Write the items: one block per image with a unique id that becomes the file name. 5 Render: render.py writes a light and a dark WebP and warns on clipping, size and fonts. 6 Look: every image in both themes, with contrast computed. A dashed arrow from Look back to Render reads: fix, render again. 7 Report: the files, their sizes, the signature, and what was not checked." width="100%"></picture>

</details>

### frontdoor-landing

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/scene-landing-dark.webp"><img src="assets/scene-landing.webp" alt="Illustration for frontdoor-landing: a front door for a repository with no landing page. A house with an open arched front door and warm light, and a welcome mat reading index.html. A sign on a post reads: Found a site? Stop and ask. To the right, a browser window shows a landing page with a headline, two buttons and the same door, labelled one index.html, with a small card labelled Open Graph preview." width="100%"></picture>

It looks for an existing landing page first and stops with its evidence when one counts.

<details>
<summary>Step by step</summary>

<picture><source media="(prefers-color-scheme: dark)" srcset="assets/landing-flow-dark.webp"><img src="assets/landing-flow.webp" alt="Flow of frontdoor-landing, in order. 1 Check first: is a Pages workflow, a docs site, a CNAME or a real index.html already there? If one is found, the flow goes to Stop and ask: show the evidence, then ask whether to do nothing, build elsewhere or replace. If none is found, it continues. 2 Place it: the root if it is free, docs/ if not, and say which Pages setting to switch on. 3 Learn the project: the README, brand, signature and writing rules, with labelled questions for the rest. 4 Try directions: two or three rough pages; you pick one or mix them. 5 Build: one index.html with inline CSS and JS and the repository's images. 6 Preview image: a 1200x630 PNG for Open Graph and Twitter, recomposed from the hero. 7 Verify: 390, 820 and 1280 px in light and dark, axe, then Lighthouse on mobile and desktop. 8 Report: the files written, the Pages setting to switch on, what was not observed, and no commit." width="100%"></picture>

</details>

## Install

Install every skill, or one by name:

```bash
npx skills add https://github.com/the-khiem7/frontdoor.git
npx skills add https://github.com/the-khiem7/frontdoor.git --skill frontdoor-landing
```

Then ask in a plain sentence, for example "make the README nicer to read" or "add a GitHub Pages landing page".

## Requirements

- `uv` and `uvx` to run the scripts (`uvx --from playwright --with pillow python -I ...`).
- Microsoft Edge or Google Chrome already installed. Nothing is downloaded and no administrator rights are needed.
- Node.js with `npx` for the Lighthouse run in `frontdoor-landing`.

## Behaviour to know

- The skills write files and stop. They never commit or push.
- `frontdoor-landing` stops and shows its evidence when it finds an existing landing page, and asks where `index.html` should go before writing.
- No look is shipped. Each repository gets its own signature: a vector shape language, a typeface and a way of presenting, derived from what the project is. Two repositories should not come out as one design with different text.
- `frontdoor-readme` writes the complete README, and every sentence and command traces to the repository or to your answer. Every run ends with a hero banner.
- Where nobody can answer a question, a skill takes the recommended default and writes the question and the assumed answer to `questions.md`.

## Status

<details>
<summary>What was exercised and what was not</summary>

Built and exercised on Windows with Edge. A trial on two real repositories, run with and without the skills, was preferred by a person for both the landing page and the README illustrations. Not yet observed: selection from a plain request, macOS or Linux, a page on its live GitHub Pages URL.

</details>

Scope, decisions and open questions live in [docs/baseline/frontdoor/](docs/baseline/frontdoor/) for the skills and in [docs/baseline/readme-design/](docs/baseline/readme-design/) for the README pictures. The pictures above are rendered from [assets/source/readme.html](assets/source/readme.html) and [assets/source/scenes.html](assets/source/scenes.html).
