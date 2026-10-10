---
name: doorway-illustrate
description: Turn hand-built HTML pages into crisp, rounded, bordered WebP illustrations in a light and a dark theme, ready for a README, a docs page or a landing page. Use whenever the user wants diagrams, workflow figures, feature cards, navigation buttons, social preview images or any "picture of a page" produced from HTML, wants light/dark image pairs, wants PNG screenshots converted to small WebP files, or asks to render, re-shoot or regenerate illustrations from an existing assets/source folder, even if they never say "WebP" or "render".
---

# Illustration render

An illustration here is an HTML block that is designed like a web page, screenshotted at 2x, finished with a rounded border and saved as lossless WebP. Rendering from HTML keeps the brand's real fonts, lets one source produce a light and a dark image from the same markup, and makes every later edit a text edit plus one command.

The look belongs to the brand being illustrated. This skill fixes the contract between a source page and the renderer, not a style.

## Workflow

1. **Find the brand.** Read the repo's logo, banner, existing CSS or docs site, app theme tokens, and its README tone. Pull out the palette, the font families, the corner radius, the mood. When the evidence disagrees (the code's theme is one blue, the icon and screenshots are teal), pick the one visitors actually see, which is usually the icon and the screenshots, and say which you chose. If the repo has no brand evidence at all, ask the user for a direction before designing anything. Do not default to this skill's starter colors: they are placeholders.
2. **Set up the source folder.** Before choosing it, check which folders the repo's linter, formatter, docs site and Docker context cover: sources placed where a linter runs get linted in CI, and files in a docs site's public folder are published. Pick `assets/source/` or the folder the repo already uses, or one that those tools ignore. Copy `assets/starter.css` to `shared.css` and `assets/shared.js` to `shared.js` from this skill, then replace the tokens, fonts and component shapes with the brand's. Keep the contract in the comment at the top of `starter.css`.
3. **Build one `.item` per image.** Each `.item` is 1200 CSS px wide with a unique `id`, because `render.py` names the file after the id. Write each source page's header comment with the exact render command so the next person can repeat it. See `references/source-page.md` for sizing, text, diagram and dark-theme rules.
4. **Render.** Run
   ```
   uvx --from playwright --with pillow python -I <skill-dir>/scripts/render.py <page.html> --root <assets dir> --out <assets dir>
   ```
   `--items a,b` renders a subset, `--themes light` skips the dark pair. The script uses Edge or Chrome already on the machine, so nothing is downloaded and no admin rights are needed. It exits 1 and prints a WARN when content leaves an item's box or a file is over `--max-kb` (default 300).
5. **Look at every image.** Open each WebP with the image viewer you have, light and dark. The script cannot judge whether a diagram reads well, whether text is cramped, or whether the dark theme has enough contrast. Fix the source and render again.
6. **Report** the files written with their sizes, and anything not checked (for example, how the page looks on the hosting site).

## Choosing how to take the screenshot

`render.py` is the default because it needs no MCP server and writes anywhere. If the user prefers a browser MCP, the same contract holds: serve the folder, open `<page>?theme=light|dark`, screenshot each `.item` at CSS scale, then run the finishing step from `render.py` (`round_and_border`) on the PNG. Some browser tools only write inside the repo root, so keep intermediates in a temporary folder there and delete it afterward.

## Pitfalls that cost time before

- A page opened as a plain file has no `?theme=` and no relative-path server, so fonts and `../logo.png` can fail. Always render through the script, which serves the folder over HTTP.
- Web fonts load from the network. Run the render online, or the fallback font silently ends up in every image. A brand that uses system fonts has the opposite problem: the fonts must be installed on the machine that renders, and a different machine will render different images.
- Do not stop to ask when nobody can answer (an automated run, a test): take the recommended default, write each question with the answer you assumed to a `questions.md` beside the output, and go on.
- Text inside an image cannot be selected or searched. Every illustration that carries information needs an `alt` text that says the same thing in words; the doorway-readme skill covers how.
- Do not commit the intermediate PNGs. Only the `.webp` files and the HTML sources belong in the repo.
