# The design board

Every design choice that needs the user's eye goes onto one local board per repository, `.frontdoor/board/index.html`, a page the user opens with a double click. The board is split into pages, one per use case (`readme`, `icons`, `navbar`, `landing-page`), and each page numbers its own rounds from 1, so icons drawn in the middle of README work start at round 1 of their own page. `fd` writes everything under `.frontdoor/board/` and adds `.frontdoor/` to `.gitignore`; nothing on the board is committed.

Below, `fd` stands for `uvx python -I <frontdoor-core>/scripts/fd.py` for the board commands and `uvx --from playwright --with pillow python -I <frontdoor-core>/scripts/fd.py` for `render` and `animate`. Run it from inside the repository being worked on.

## One round

1. **Pick the page.** Use the page of the work you were asked for. `fd status` lists the pages; add a missing one with `fd page add <slug> --title "<what it is for>"`. A slug is lowercase letters, digits and hyphens. When a skill is called by another, it uses the caller's page.
2. **Ask how many variants.** Ask the user every round, with a recommendation: a wide first round of a new look wants more, a refinement of a chosen direction fewer. Never assume a number. With no user to answer (an automated run), make 3 and write the question with that answer to `questions.md`.
3. **Ask about a variant-against-variant comparison** only when two variants differ in one detail the user must judge side by side; it is off unless the user wants it, and then set `"compare": true` in `round.json`. Light against dark is always shown.
4. **Start the round.** `fd round new <page> --count <N> --title "<what this round answers>"` creates `.frontdoor/board/<page>/round-<n>/` with one folder per variant (`a/`, `b/`, ...) and `round.json`. `--seed <file>` copies a starting file, such as the core's `assets/starter.html`, into every variant folder.
5. **Build each variant in its folder.** Rough and low fidelity, each with a different idea, not one idea in three colours. Render pictures into `<variant>/out/` with `fd render <variant>/<page>.html --out <variant>/out`; a page variant is `<variant>/index.html`, and a screenshot of it goes into `<variant>/out/` too.
6. **Write the round.** Fill `round.json`: the round's `title` and `note` (what it answers), and per variant a `title`, the `concept` in one or two sentences, `strengths`, `risks` and the `flaws` you already know. State the risks of a variant you like as plainly as those of one you do not.
7. **Publish it.** `fd round add <page>` reads `round.json`, finds each variant's pictures in `out/` (or in the variant folder when it has no `out/`), pairs `<name>.webp` or `<name>-light.webp` with `<name>-dark.webp` into one picture with both themes, links `index.html` when there is one, rebuilds the board and prints what it found. It stops and names every variant that has no title or nothing to show. List `images` or `links` in a variant of `round.json` only to override what it finds.
8. **Show it and wait.** Give the user the board path it printed, as a link, and wait for the choice. Tell them once how to answer: pick one or more variants on the board, write notes if they want, press Copy choice and paste the text into the chat. Run `fd round add` again after a change to the renders; the choice is kept.
9. **Record the choice.** When the user pastes text from the board, save it to a file and run `fd choose --from <file>` (a pipe to `fd choose --from -` works too, except from Windows PowerShell 5.1, whose pipe turns letters outside ASCII into question marks); it reads the last `fd-choice` line, so never retype the ids. When the user answers in words instead, run `fd choose <page> <round> <ids> --note "<what was mixed>"`, with `--variant-note B="<text>"` for a note on one variant; several ids record a mix. A pasted choice with no variant means the user rejected them all: start the next round from their notes.

## Reading the board without reading it

`fd status` prints one line per page: its rounds, the latest round's variants, the choice and any draft. `fd status --json` gives the same as data. Read it instead of `board.json` when you need to know where a design stands.

## What the user sees

The board opens on the newest round of the page last looked at. Each variant is a card with its picture fitted to the screen. One frame holds both themes, with a light, dark and split switch; in split mode the pointer draws the divider between the two. A click opens the picture in a viewer that fits it, fills the width or zooms, and scrolls a long picture. The rail on the left lists every page and round with the recorded choices and opens on hover. The rounds of a page are tabs. Every place has a link (`index.html#/<page>/<round>/<variant>`), so you can send the user straight to one variant. The Compare button, which shows two variants side by side with their scrolling joined, appears only on a round whose `round.json` has `"compare": true`. Picks and notes stay in the user's browser until they copy them; the record is `board.json`, written only by `fd`.

## Rules

- One board per repository, never one per skill or per purpose, and never a hosted page (a published artifact, a gist, a preview link): those leave one page per round behind in the user's account, and unreleased work may be on them.
- The board has one neutral look in every repository. It is a working tool, so it never takes the signature of the repository it serves, and a round's variants are judged on the same ground.
- `board.json` is the record. Edit it by hand only to repair it, then run `fd board build`.
