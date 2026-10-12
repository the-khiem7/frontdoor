---
name: frontdoor-illustrate
description: Draw one repository's own vector illustrations, banners, scenes and diagrams as HTML, and render them to crisp, rounded, bordered WebP in a light and a dark theme, ready for a README, a docs page or a landing page. Use whenever the user wants a hero banner, a header image, scene illustrations, workflow figures, feature cards, social preview images or any "picture of a page" produced from HTML, wants a distinctive look for a new repository, wants light/dark image pairs, wants PNG screenshots converted to small WebP files, or asks to render, re-shoot or regenerate illustrations from an existing assets/source folder, even if they never say "WebP" or "render".
---

# Illustration render

An illustration here is an HTML block that is designed like a web page, screenshotted at 2x, finished with a rounded border and saved as lossless WebP. Rendering from HTML keeps the real fonts, lets one source produce a light and a dark image from the same markup, and makes every later edit a text edit plus one command.

Every repository gets its own signature: a vector shape language, a typeface and a way of presenting, derived from what the project is. This skill ships no look. It fixes the contract between a source page and the renderer, a quality floor, and a method for finding the signature (`references/signature.md`). Two repositories that use it must not end up with one design and different text.

## Workflow

1. **Find the brand.** Read the repo's logo, banner, existing CSS or docs site, app theme tokens, and its README tone. When the evidence disagrees (the code's theme is one blue, the icon and screenshots are teal), pick the one visitors actually see, which is usually the icon and the screenshots, and say which you chose. If a signature already exists in the repo (source pages with a signature note, a hero), continue it instead of inventing another.
2. **Find the signature.** If the caller (for example `frontdoor-readme`) handed you a signature, or the repo's source pages already carry a signature note, use it and go to step 3. Otherwise, with no brand evidence or a brand that leaves the drawing style open, follow `references/signature.md` and write the six-line signature note. For a new repository, or when asked for a fresh look, make two or three rough directions (one hero each, low fidelity), show them on the local board and let the user choose or mix; build each round, with any font specimen, under `.frontdoor/round-<N>/` with its own inline CSS, and show it as `references/signature.md` says under "Show the directions". Nothing in `.frontdoor/` is committed. With no user to answer, pick the strongest yourself and write the reason to `questions.md`. Ask the user for a direction only when the repo gives you nothing to derive one from.
3. **Set up the source folder.** Before choosing it, check which folders the repo's linter, formatter, docs site and Docker context cover: sources placed where a linter runs get linted in CI, and files in a docs site's public folder are published. Pick `assets/source/` or the folder the repo already uses, or one that those tools ignore. Copy `assets/starter.css` to `shared.css` and `assets/shared.js` to `shared.js` from this skill, then replace the tokens and the font with the signature's, add the shapes it needs, and delete the `--starter-placeholder` line. Put the signature note in the header comment of each source page.
4. **Build one `.item` per image.** Each `.item` is 1200 CSS px wide with a unique `id`, because `render.py` names the file after the id. Write each source page's header comment with the exact render command so the next person can repeat it. Choose a scene or a diagram per picture with `references/scene-craft.md`. See `references/source-page.md` for the contract, the quality floor, and the craft notes.
5. **Render.** Run
   ```
   uvx --from playwright --with pillow python -I <skill-dir>/scripts/render.py <page.html> --root <assets dir> --out <assets dir>
   ```
   `--root` is the folder the script serves; it must contain the source page, `shared.css` and `shared.js`, and the folder the output goes to. With sources in `assets/source/` and images in `assets/`, use `--root assets --out assets`. `--items a,b` renders a subset, `--themes light` skips the dark pair. The script uses Edge or Chrome already on the machine, so nothing is downloaded and no admin rights are needed. It exits 1 and prints a WARN when content leaves an item's box, a file is over `--max-kb` (default 300), a font was requested but did not load, or the starter placeholder is still served. It prints the fonts and grounds it found; copy them into the signature note. It checks the item's own box, not a card or node inside it, so a label that runs out of its card passes silently: look at every image. A shape meant to run off the edge goes inside an element marked `data-bleed`.
6. **Look at every image.** Open each WebP with the image viewer you have, light and dark. The script cannot judge whether a picture reads well or whether text is cramped. Compute the contrast of the smallest text pairs in both themes with `uvx python -I <skill-dir>/scripts/contrast.py <fg> <bg> [...]`. Run the swap test from `references/signature.md`. Fix the source and render again.
7. **Report** the files written with their sizes, the signature in its six lines, and anything not checked (for example, how the page looks on the hosting site).

## Choosing how to take the screenshot

`render.py` is the default because it needs no MCP server and writes anywhere. If the user prefers a browser MCP, the same contract holds: serve the folder, open `<page>?theme=light|dark`, screenshot each `.item` at CSS scale, then run the finishing step from `render.py` (`round_and_border`) on the PNG. Some browser tools only write inside the repo root, so keep intermediates in a temporary folder there and delete it afterward.

## Pitfalls that cost time before

- A page opened as a plain file has no `?theme=` and no relative-path server, so fonts and `../logo.png` can fail. Always render through the script, which serves the folder over HTTP.
- Web fonts load from the network. Render online; `render.py` warns when a requested font did not load and a fallback face is in the images. A repository that uses system fonts has the opposite problem: the fonts must be installed on the machine that renders, and a different machine will render different images. Load only open-license families from a font host, or the repository's own fonts; never copy a font file into the skill or the repo without its license.
- Do not stop to ask when nobody can answer (an automated run, a test): take the recommended default, write each question with the answer you assumed to a `questions.md` beside the output, and go on.
- Text inside an image cannot be selected or searched. Every illustration that carries information needs an `alt` text that says the same thing in words; the frontdoor-readme skill covers how.
- Do not commit the intermediate PNGs. Only the `.webp` files and the HTML sources belong in the repo.
