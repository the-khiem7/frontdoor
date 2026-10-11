# Writing a source page

Read this when building or fixing an `.item`. The page has two kinds of rules. The contract with `render.py` is hard: break it and the render fails or comes out wrong. The craft notes are soft: each carries its reason so you can drop it when the picture is better for it. How the pictures look is not in this file; that comes from the signature (`signature.md`).

## The contract with `render.py` (hard)

| Rule | Why |
|---|---|
| Each image is a `.item` with a unique `id`, inside `.sheet` | the id is the output file name; `render.py` stops when one is missing |
| `.item` has `width: 1200px; zoom: 2` | 1200 CSS px becomes a 2400 px image; the README column is about 830 px, so the image still has 2x density |
| Theming only through `html[data-theme="dark"]` | `shared.js` sets it from `?theme=`; any other mechanism renders both themes identically |
| `--cardline` is defined in both themes | the script reads it as the border color of the finished image; without it a fallback gray-blue is used |
| Source pages sit beside `shared.css` and `shared.js` | relative links resolve because the whole folder is served |
| The `--starter-placeholder` line is deleted from the stylesheet | while it is served, `render.py` warns that the starter's values are still in use |

## Quality floor (hard, with a reason)

- Text is readable: about 17 CSS px at the smallest, because at the README's 830 px column that is about 12 px on screen, the floor for reading without squinting.
- Contrast is computed, not judged, for the smallest text in both themes, because that is where it fails first. `scripts/contrast.py` prints the ratio of color pairs.
- A picture states only what the README or the code states, because a figure is where an invented claim hides.
- The README's own rules apply to the picture: no skill or command counts if it bans them, no typographic dashes if it bans them.

## Craft notes (soft)

- **Height.** Height is per item. Set it explicitly and leave 30 to 40 px of air under the last element; an item that ends exactly at its content looks cut off at the border.
- **Short text.** Short sentences in cards. If a card needs three lines, the idea probably wants two cards.
- **Navigation buttons** are a small item (for example 200x56 CSS px) with large text, shown at a fixed height in the README. They are optional; plain anchors often serve better.
- **Scenes and diagrams.** Choosing between them, building them and the SVG techniques are in `scene-craft.md`.
- **Logo or icon across items.** An `<img>` cannot change color per theme. Put the mark in one inline SVG sprite (`<symbol id="mark">`) injected by `shared.js` or pasted into each page, and reference it with `<use href="#mark">` so it takes `currentColor` or a token.
- **Ring and mask shapes.** A circular progress ring built with a `mask` or `conic-gradient` needs `border-radius: 50%` on the element, or the clipped corners render square. Check it in the PNG, not only in the browser.
- **Chips and labels.** A label or chip that sits across a card's edge reads as a mistake. Keep every chip inside its card and put branch labels on the line.
- **Look at every image** at full size, light and dark, before reporting.

## Dark theme

- Redefine every color token, not only the background. A card that keeps its light fill on a dark sheet is the usual miss.
- Raise the accent a step in the dark theme: the same saturated color that looks crisp on paper looks muddy on a dark ground.
- Pure white text on dark is harsh; use the same off-white you would use for body text on the brand's dark pages.
- A mark drawn with a dark token vanishes on a dark ground. Give each kind of mark its own token and set it in both themes.

## When render.py prints a WARN

| WARN | Meaning | Fix |
|---|---|---|
| `content leaves the item box: x, y` | an element extends past the item's edge, so it is clipped in the image | shorten the text, widen the box or raise the item height; a shape meant to run off the edge goes inside an element marked `data-bleed`. The check sees the item's box only, not a card inside it |
| `over 300 KB` | lossless WebP of a busy image grew large | simplify gradients and lines first; use a lossy re-encode only for the image that still exceeds the budget, and say so |
| `fonts requested but not loaded` | a font family in the page did not load, so a fallback face is in every image | render online, install the font, or load it from a font host; check the family name |
| `starter placeholder tokens are still in use` | the stylesheet still carries the starter's values | replace the tokens and the font with the repository's own and delete the `--starter-placeholder` line |

The run also prints the fonts and the page grounds it found. Copy them into the signature note at the top of the source page.
