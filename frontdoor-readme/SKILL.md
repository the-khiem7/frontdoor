---
name: frontdoor-readme
description: Plan and carry out a visual upgrade of a repository's README, replacing walls of text, ASCII diagrams and plain Mermaid with designed illustrations, light/dark image pairs, image buttons and a scannable section order. Use whenever the user wants a README to look better, be easier to scan, "pop", get diagrams, a workflow figure, use-case visuals, navigation buttons or a banner-matching redesign, or says a README is a wall of text, even if they only mention one of these. Hands the actual image building to the frontdoor-illustrate skill.
---

# README visualization

A README is read in the first 30 seconds by someone deciding whether to keep reading. Pictures earn their place when they carry the answer to a question that text answers slowly: what problem is this, how does the work flow, which part do I use for my situation. Pictures used as decoration lower trust and cost reading time.

## Workflow

1. **Audit before designing.** Read the whole README, the banner or logo, any docs site, `AGENTS.md` / `CONTRIBUTING.md` and the tests that read the README (see "Repo rules that bite"). Find which folders the linter, the docs site and the Docker context cover, so the image sources and files do not land where they are linted or published by accident. Write down, for each section, the reader's question it answers and whether the answer is a sequence, a comparison, a structure or a lookup. Only sequences and structures become pictures; lookups stay tables.
2. **Find the brand and ask what is open.** Colors, fonts, corner style and mood come from the repo's own banner and docs. Ask the user a few labelled questions (grouped by topic, each with options and a recommended default) about what the repo cannot answer: how far to go, the language of the images, whether to keep a text form of each diagram, light/dark pairs or one image. Do not ask what the repo already shows. When nobody can answer (an automated run, a test), take the recommended default for each, write the question with your assumed answer to a `questions.md`, and continue.
3. **Propose the plan before building.** List the sections in their new order, which ones get an image and of what kind, which stay text, what moves into `<details>`, and the files that will be added. Wait for approval; a redesign touches the page every visitor sees. See `references/audit-and-plan.md` for the shape of the plan and the usual mapping from content to figure.
4. **Build the images with `frontdoor-illustrate`.** Hand it the list of items with their content. Keep text in the images identical in meaning to the README text they replace; do not invent claims to fill a figure.
5. **Rewrite the README.** Markup patterns, alt-text rules and what GitHub strips are in `references/github-readme.md`. Move reference material below the visual sections instead of deleting it.
6. **Verify.** Run the repo's tests. Check every image path, every anchor, that headings exist for each navigation link, and that no image carries a fact the README does not. Say plainly what was not observed: the README on the hosting site in light and dark, and on a phone.
7. **Record, do not commit.** Leave the work in the working tree unless the user asks for a commit. If the repo keeps a decision log, offer to write the decision down with what was rejected and the costs accepted.

## Creative latitude

The user wants taste, not a template. Choose the visual language from the brand: a playful project can use hand-drawn cards, a serious infrastructure tool a quiet grid. What is not negotiable is the reader's path: problem, then how it works, then which part is for me, then how to start, then reference.

## Repo rules that bite

- A test may scan the README for identifier-shaped tokens or typographic dashes; read the repo's tests and conventions first. A diagram example such as an entry id belongs inside an image, not in alt text, if such a test exists.
- If the repo states counts in prose (number of skills, commands), do not put a count in an image either.
- Install instructions and commands stay as text so they can be copied.
- Image buttons for navigation are optional. When the number of illustrations is capped, or the page already has many figures, plain text anchors are a fine default; spend the images on figures.
- Diagrams must match what the code or product actually does. Check each branch of a flow figure against the source, not the README alone, and say in the report which branches you could not check.
