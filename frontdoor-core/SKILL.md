---
name: frontdoor-core
description: The frontdoor principles and harness for visual design work in a repository - a signature derived from the project instead of a template look, rough variants shown on one local design board with a page per use case, the number of variants asked every round, pictures rendered from HTML to light and dark images of any size, and the `fd` command that does the repeated steps. Use whenever the user wants to apply the frontdoor approach, design board or variants to work no other frontdoor skill covers, such as redesigning a component of a web page, drawing icons or comparing UI directions, or asks to put options on the design board, render HTML to light and dark images, or start the frontdoor render daemon. The other frontdoor skills read it for these steps.
---

# Frontdoor core

The frontdoor skills share one way of doing visual work. This skill holds it, so it can be applied to any design task, not only a README or a landing page.

## Principles

- **A signature, not a template.** Every repository gets its own vector shape language, typeface and way of presenting, derived from what the project is. Follow `references/signature.md`. Never reuse another repository's look, the examples in that file or the look of the frontdoor repository itself. When the repository already has a brand or a signature, continue it.
- **Show variants before building one.** A design choice the user has to make goes onto the design board as a round of rough variants. Ask how many variants every round, with a recommendation; never assume a number. The method is `references/board.md`.
- **Truthful pictures.** A picture states only what the code or the docs state, follows the repository's own writing rules, and carries an alt text that says the same in words.
- **Measured, not judged.** Compute contrast (`fd contrast`), read the fonts and warnings `fd render` prints, and look at every image in both themes at the size it ships at.
- **Write files and stop.** Never commit or push. Nothing under `.frontdoor/` is committed.
- **Unattended runs.** Where a step says to ask and nobody can answer, take the recommended default, write each question with the answer you assumed to `questions.md`, and continue.

## Workflow

1. **Read the repository.** Its code, docs, existing brand (logo, banner, CSS, theme tokens), `AGENTS.md` or `CONTRIBUTING.md`, and the tests that read documentation. Find which folders the linter, the docs site and the Docker context cover, so sources and images do not land where they are linted or published by accident.
2. **Find the signature** with `references/signature.md`, or continue the one the repository has. A caller that hands you a signature has already done this step.
3. **Run rounds on the board** as `references/board.md` says: pick the page, ask the number of variants, `fd round new`, build and render each variant, fill `round.json`, `fd round add`, show the board path and wait, `fd choose`.
4. **Build the chosen design** in the place the repository uses. Pictures are HTML source pages rendered by `fd render`; their contract (item size, finish, theming) is in `references/source-page.md`, and `assets/starter.css`, `assets/starter.html` and `assets/shared.js` are the starting files. A moving picture is made with `fd animate`, as a looping animated WebP, never a GIF.
5. **Verify and report.** List the files written with their sizes, the signature in its six lines, the checks run, and what was not observed.

## The harness

`fd` is `scripts/fd.py`, run with `uvx`; `references/harness.md` lists every command and how to run it. When a task renders more than a few times, start `fd daemon start` first so one browser stays open, and use `fd render --watch` while editing a source page.
