# Signature

A signature is what makes one repository's pictures impossible to mistake for another's: the shape language of its vector drawings, its typeface, and how it presents (composition and story). Derive it from the repository. Never choose it from this file: the examples below show the method, and a copied example is the failure this file exists to prevent.

## Derive it

1. **Subject.** What the project is, who uses it, what using it feels like. Read the code, the docs, the README and any existing brand.
2. **Metaphor.** One physical or cultural image for the subject, not the logo of the technology it uses.
3. **Shape language.** How the metaphor becomes forms: stroke weight, corners, density, flat or layered, perspective or none, whether drawings carry characters or only objects.
4. **Typeface.** A pairing that carries the mood, from fonts you can load (an open-license family on a font host, or the repository's own). Put three candidates in a specimen item, render it and look before choosing.
5. **Palette logic.** Where the color comes from (the subject, the brand, the metaphor), which color does the work, how both themes keep the same mood.
6. **Presentation.** How a picture tells its story: a scene, a diagram, a strip, a poster; how much text; what voice the text has.
7. **What it is not.** What you deliberately avoided, in one line.

Write the signature note as six lines at the top of the source page, so the next edit stays inside the signature: the concept (steps 1 and 2 in one line), the shape language, the typeface, the palette logic, the presentation, and what it is not.

## Keep it from being generic

- Think of three signatures and discard the most obvious one. The first idea that comes to mind is the average of every other repository's.
- Swap test: replace the project's name and text with another project's. If the pictures still fit, they are generic. Redo them.
- Treat these as defaults to leave: the starter's tokens, a system or most-used UI typeface as the display face (and the characterful serifs and grotesques that every agent reaches for first: Fraunces, Playfair Display, Space Grotesk, Inter), one blue-purple gradient, rounded cards with a soft shadow as the only shape, stock icon sets.
- Do not reuse another repository's signature, including the examples here and the look of the frontdoor repository's own pictures (an arched doorway, warm amber light, a paper and a night theme). That look answers one subject.

## Examples of the method

Each pairs a subject with a signature derived from it. They differ on purpose. A project of the same kind as an example must still derive its own: the example shows how a subject becomes a look, not what that kind of project looks like.

| Subject | Signature in one line |
|---|---|
| A library that parses subtitle files | editing-room splice table: film strips, tape marks, grease-pencil notes, a condensed gothic with a hand-lettered accent, grey film base with one marker color, pictures laid out as a contact sheet |
| A tool that rotates secrets | clockwork: gears and a ratchet drawn as flat outlines, engraved serif capitals, warm metal on deep green, pictures composed as exploded parts diagrams |
| A compiler for a tiny language | origami: creased paper planes with shadows only at the folds, a geometric sans with chunky numerals, two paper colors per theme, steps drawn as a crease pattern |
| A ferry timetable service | harbor signal flags: bold flag blocks and rope lines, a stencil sans, maritime primaries on sand, scenes composed as a harbor master's board |
| A tool that renames photographs | star chart: dot-and-line figures on a deep ground, italic serif names, numbered plates, pictures as sheets from an atlas |
| A fuzzing tool | linocut: heavy carved black lines, rough edges, one ink and one paper, a blunt slab display face, pictures as prints on a wall |

## Show the directions

Two or three rough directions go on one local board, never onto a hosted page and never as a list of file paths. The board is `.frontdoor/directions.html` in the repository being worked on, a page the user opens with a double click. Every round goes onto the same board, newest first, so a design that takes many rounds stays in one place and the user can compare rounds.

1. Build each round under `.frontdoor/round-<N>/`: the rough sources, any font specimen and the renders (for a landing page, one folder per direction and its `shoot.py` screenshots). Render with `--root .frontdoor/round-<N> --out .frontdoor/round-<N>/out`.
2. Describe the round in a JSON file kept outside `.frontdoor/`, in your session's scratch area: a title, a note on what the round answers and, per direction, a title, the concept in one or two sentences, strengths, risks, the flaws you already know, and the images (a label and a path relative to `.frontdoor/`, one per theme) or a link to the local page. State the risks of a direction you like as plainly as those of one you do not. The exact shape is in the docstring of `scripts/board.py`.
3. Run `uvx python -I <skill-dir>/scripts/board.py add .frontdoor <round.json>`. It appends the round, rebuilds the board, opens it in the default browser and prints the path. It also adds `.frontdoor/` to the repository's `.gitignore` when the entry is missing, so the board and the sketches are never committed. Repeat the path in your message as a link and wait for the choice.
4. When the user chooses or mixes, run `board.py choose .frontdoor <round> <ids> --note "<what was mixed>"`. After a hand edit of `.frontdoor/directions.json`, run `board.py build .frontdoor`. Add `--inline` to get one file that embeds its images, for sending, and `--no-open` where nothing can open a browser.

Do not publish the board. The sketches are scratch, a hosted page (a published artifact, a gist, a preview link) leaves one page per round behind in the user's account, and unreleased work may be on it.

## Check before you report

- State the signature in the six lines above and keep them in the source page.
- Every round of directions is on the board, and neither the board nor the sketches are tracked by git.
- Run the swap test and read the defaults list against the pictures.
- Read the fonts that `render.py` printed: a requested font it warns about did not load, and a fallback face is in the images.
