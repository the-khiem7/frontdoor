---
name: frontdoor-readme
description: Write or rewrite a repository's complete README around vector illustration - a hero banner, scenes that tell the project's story, diagrams where they fit, light and dark image pairs, and a scannable layout with details blocks where suitable - in a look drawn from that one repository. Use whenever the user wants a README written, rewritten, redesigned or made nicer to read, a new repository needs a README, a banner or a visual identity, or says a README is a wall of text, plain, or looks like every other one, even if they only mention one of these. Uses the frontdoor-illustrate skill for the image building when it is available.
---

# README design

A README is read in the first 30 seconds by someone deciding whether to keep reading. Pictures earn their place when they carry the answer to a question that text answers slowly: what is this, what is it like to use, which part is for me. Pictures used as decoration lower trust and cost reading time.

The target of this workflow is a finished README: complete text, a hero banner and illustrations that belong to this repository alone. Not a skeleton, and not a template with the name swapped.

## Workflow

1. **Audit and classify.** Read the code, the manifests, the scripts, the CI, the tests and any docs, then the existing README, the banner or logo, `AGENTS.md` / `CONTRIBUTING.md` and the tests that read the README (see "Repo rules that bite"). Find which folders the linter, the docs site and the Docker context cover, so the image sources and files do not land where they are linted or published by accident. Classify the repository:
   - **greenfield**: no README or only a draft, and no brand evidence (banner, logo, CSS, docs site). The signature is invented from the subject.
   - **brownfield**: anything else. Read the brand that exists and continue it.
2. **Collect the facts, then ask what is open.** Read `references/readme-content.md` and build a fact list: for each thing the README will say, where in the repo it comes from. Ask the user a few labelled questions (grouped by topic, each with options and a recommended default) about what the repo cannot answer: the purpose or audience when the code does not say, the tone, the language, how far to go, whether to keep a text form of each diagram. Do not ask what the repo already shows. When nobody can answer (an automated run, a test), take the recommended default for each, write the question with your assumed answer to a `questions.md`, and continue.
3. **Find the signature and the hero.** Follow `references/signature.md`: a vector shape language, a typeface and a way of presenting, derived from this repository's subject. A hero banner ends every run, in both modes. You own the signature and the rough directions in this skill; hand the chosen signature to `frontdoor-illustrate` in step 5 so it does not start over. Greenfield: invent the signature, and show two or three rough hero directions (low fidelity, built with any font specimen under `.frontdoor/round-<N>/` and shown on the local board that `references/signature.md` describes under "Show the directions"; nothing in `.frontdoor/` is committed) for the user to choose or mix; with no user to answer, pick the strongest and write the reason to `questions.md`. Brownfield: assess the banner that exists against the repository's signature; keep it when it fits and say so in the plan; when it does not fit (low resolution, no dark version, off-brand), propose a replacement and wait for approval. The rough directions are optional in a brownfield repository.
4. **Propose the plan before building.** List the sections in their new order, which ones get a scene, a diagram or stay text, what goes into `<details>`, the hero, the fact list, and the files that will be added. Wait for approval; a README is the page every visitor sees. With no user to answer, write the plan to `questions.md` with the default taken, and continue. See `references/audit-and-plan.md` for how to choose a figure per section.
5. **Build the images with `frontdoor-illustrate` when it is available.** Hand it the signature and the list of items with their content. When it is not installed, say so and ask the user how the images should be produced; the skill must still run alone. Keep text in the images identical in meaning to the README text they replace; do not invent claims to fill a figure.
6. **Write the README.** Write it complete: what the project is and for whom, the problem it solves, what it does, how to install and use it, what it needs, and the parts a reader of that kind of project expects. Every sentence and every command traces to the fact list. Markup patterns, alt-text rules, `<details>` and what GitHub strips are in `references/github-readme.md`. Move reference material below the visual sections instead of deleting it.
7. **Verify.** Run the repo's tests; when it has none, or running them would need installing its dependencies, say so instead. Check every image path, every anchor, that headings exist for each navigation link, that no image carries a fact the README does not, and that every sentence and command traces to a source; install and run commands come from the manifest, the scripts or the CI, not from memory. Say plainly what was not observed: the README on the hosting site in light and dark, and on a phone.
8. **Record, do not commit.** Leave the work in the working tree unless the user asks for a commit. If the repo keeps a decision log, offer to write the decision down with what was rejected and the costs accepted.

## Creative latitude

The user wants taste, not a template. The signature is the point of this skill family: the shape language, the typeface and the presentation of one repository must not be mistakable for another's. A playful project can use hand-cut collage, a serious infrastructure tool a survey-map grid; what each looks like is yours to derive. Do not reuse the look of an earlier run or of the frontdoor repository itself. What is not negotiable is the reader's path: what this is, how it works, which part is for me, how to start, then reference.

## Repo rules that bite

- A test may scan the README for identifier-shaped tokens or typographic dashes; read the repo's tests and conventions first. A diagram example such as an entry id belongs inside an image, not in alt text, if such a test exists.
- If the repo states counts in prose (number of skills, commands), do not put a count in an image either.
- A scene may be a metaphor, but what it claims the product does, and every label in it, come from the code. Do not draw an effect the code does not produce.
- A count drawn as objects (two stones for two stories) is a count too: draw a number of objects that is not a real count, or avoid objects that add up.
- Install instructions and commands stay as text so they can be copied, and are never hidden inside `<details>`.
- Image buttons for navigation are optional. When the number of illustrations is capped, or the page already has many figures, plain text anchors are a fine default; spend the images on figures.
- Diagrams must match what the code or product actually does. Check each branch of a flow figure against the source, not the README alone, and say in the report which branches you could not check.
