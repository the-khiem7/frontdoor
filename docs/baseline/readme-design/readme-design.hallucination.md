---
baseline_schema: "2.0"
pack: "readme-design"
document: "hallucination"
status: "active"
updated: "2026-10-11"
code_ref: "uncommitted"
---

# README design: Decisions and Open Questions

## Entry index

One row per entry. A row states what the entry is about and nothing more. An answer that turns on an entry whose full text was not read is unbacked.

| Entry | About | Status | Related |
|---|---|---|---|
| RD-D1 | how the README pictures are produced and where the sources and files live | current | FD-D3 |
| RD-D2 | the look of the pictures: an arched doorway in a paper and a night theme | current | RD-D1, FD-D5 |
| RD-D3 | what each skill shows in the README: a scene, with its step-box flow inside `<details>` | current | RD-D1, RD-D2, FD-D16 |
| RD-Q1 | whether the README renders as designed on github.com in light, dark and on a phone | open | RD-D1, RD-D3 |
| RD-Q2 | whether `npx skills add` skips the root `assets/` folder | open | RD-D1 |

## RD-D1: the README pictures are rendered from two HTML source pages into `assets/`

Decision: render `hero`, `skills-map`, `readme-flow`, `illustrate-flow` and `landing-flow` from `assets/source/readme.html`, and `scene-readme`, `scene-illustrate` and `scene-landing` from `assets/source/scenes.html`, with `render.py` into `assets/<id>.webp` and `assets/<id>-dark.webp` - a text edit plus one command regenerates them (FD-D3, pack frontdoor), and the folder sits outside every skill folder, so nothing in it travels with `npx skills add`.

What breaks if ignored: a flow or a scene restates `SKILL.md` steps and the optional-help rule and nothing compares them, so a changed step leaves it stale; `skills-map` draws one card per skill, so a skill added or removed needs a source edit and a render. Rendering offline puts fallback fonts into every image with no warning. The flows of `frontdoor-readme` and `frontdoor-illustrate` exist only in their `SKILL.md`, so the alt text in the README is their only text form there.

Measured: sixteen files; the flows, hero and map are 59 to 90 KB each, about 720 KB in all; the scenes are 92 to 122 KB each, about 630 KB in all; `render.py` exit 0 with no WARN for both pages. Every image was looked at in both themes.

Rejected: two figures (`hero` and `skills-map`) - the user chose a flow for each skill as well.

Rejected: image buttons for navigation - the README has few sections and plain headings serve.

Rejected: `docs/readme/` for the files (the recommended folder) - the user chose a root `assets/`, which shares its name with each skill's own `assets/`; `AGENTS.md` carries a row that tells them apart.

## RD-D2: the pictures use an arched-doorway look in a paper and a night theme

Decision: draw the README pictures as an arched doorway with warm light - paper theme (ground `#faf5ea`) and night theme (ground `#11151d`); amber for shapes and strokes only, `#8a4f06` for small amber text on paper; Fraunces for display, DM Sans for text, JetBrains Mono for names and labels, fetched from Google Fonts at render time - the repository had no banner, logo, CSS or docs site and the user left the direction open, so the look is invented here and belongs to these pictures, not to the skills (FD-D5, pack frontdoor).

What breaks if ignored: pale amber as small text on the paper theme is too light to read; a render without network puts fallback fonts into every image (RD-D1).

Measured: computed contrast of the text color pairs, lowest 5.15 (tag text on the ground band), after the color of strings in the code window was lightened from 4.22 (`#8fc29c`, not recomputed).

Rejected: a quiet GitHub-neutral look with one amber accent (the recommended direction) - the user asked for a creative look.

## RD-D3: each skill shows a scene, and its step-box flow moves into `<details>`

Decision: show each skill as a scene, a flat vector illustration in the doorway world, and keep its step-box flow inside `<details>` under it - the user found the step-box flows heavy and asked for vector illustration to reach the reader.

Scenes: one story per skill: a pile of text through the door into a README (`frontdoor-readme`), an HTML block through a camera into a light and a dark picture (`frontdoor-illustrate`), a house with an open door, a browser page and a sign that says to stop and ask (`frontdoor-landing`). The pictures drawn inside a scene use fixed colors, not theme tokens, because they depict a light and a dark picture.

What breaks if ignored: a scene restates what a skill does and nothing compares them (RD-D1); a picture inside a scene drawn with theme tokens stops showing a light picture and a dark picture side by side. The `frontdoor-readme` scene and the `skills-map` figure both show the render skill as optional help, which holds only because step 4 of `frontdoor-readme` says so (FD-D16, pack frontdoor).

Rejected: the step-box flows as the main figure of each skill - the user found them heavy and asked for vector illustration to reach the reader; the flows stay in `<details>`, so no step or gate is lost.

Rejected: dropping the flows from the README once the scenes existed - the wait-for-approval gate and the stop-and-ask branch would then live only in `SKILL.md`.

## Open questions

### RD-Q1: does the README render as designed on github.com in light, dark and on a phone?

Nothing was viewed on the hosting site. Not observed: the dark `<source>` swap, `<picture>` inside `<details>` (the flows) and inside an `<h1>` (the hero), and the pictures at a phone's width. What is at stake: a broken swap or a collapsed flow degrades the page every visitor sees first. Trigger to close: open the README on a pushed branch or the repository page in both color schemes and on a phone.

### RD-Q2: does `npx skills add` skip the root `assets/` folder?

`npx skills add --list` found the skills by their `SKILL.md` before the folder existed; it was not run again once `assets/` was added. What is at stake: an install that picks up the README pictures, or mistakes the folder for a skill, puts files into the user's repository that no skill asked for. Trigger to close: run `npx skills add <repository> --list` and a single-skill install after `assets/` is pushed.
