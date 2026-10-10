# Writing a source page

Read this when building or fixing an `.item`. Every number below came from a failure; the reason is given so you can judge when a different number is right.

## The contract with `render.py`

| Rule | Why |
|---|---|
| Each image is a `.item` with a unique `id`, inside `.sheet` | the id is the output file name; `render.py` stops when one is missing |
| `.item` has `width: 1200px; zoom: 2` | 1200 CSS px becomes a 2400 px image; the README column is about 830 px, so the image still has 2x density |
| Theming only through `html[data-theme="dark"]` | `shared.js` sets it from `?theme=`; any other mechanism renders both themes identically |
| `--cardline` is defined in both themes | the script reads it as the border color of the finished image; without it a fallback gray-blue is used |
| Source pages sit beside `shared.css` and `shared.js` | relative links resolve because the whole folder is served |

## Size and text

- Height is per item. Set it explicitly and leave 30 to 40 px of air under the last element; an item that ends exactly at its content looks cut off at the border.
- Smallest text is 17 CSS px, 18 to 20 for descriptions. At the README's 830 px column that is about 12 px on screen, the floor for reading without squinting. Smaller text in a pretty diagram is the commonest reason a figure is ignored.
- Short sentences in cards. If a card needs three lines, the idea probably wants two cards.
- Navigation buttons are the exception: a small item (for example 200x56 CSS px) with large text, shown at a fixed height in the README.

## Diagrams

- Inline SVG inside the `.item` is fine because it uses the page's fonts. Use `text-anchor: middle` and place text by its center.
- Draw arrows after the boxes they connect and check that no arrowhead is hidden behind a box. Offsetting a connector by a few px is cheaper than redrawing.
- Put labels on branches ("yes", "no") at the line, not in a legend.
- Keep one idea per image. A workflow with more than about eleven nodes should be two figures.

## Reusing a logo or icon across items

An `<img>` cannot change color per theme. Put the mark in one inline SVG sprite (`<symbol id="mark">`) injected by `shared.js` or pasted into each page, and reference it with `<use href="#mark">` so it takes `currentColor` or a token.

## Ring and mask shapes

A circular progress ring built with a `mask` or `conic-gradient` needs `border-radius: 50%` on the element, or the clipped corners render square. Check it in the PNG, not only in the browser.

## Legibility checks the script cannot do

- A label or chip that sits across a card's edge reads as a mistake. Put branch labels on the line, and keep every chip inside its card.
- A small icon at the left of each card makes a grid of cards much faster to scan than text alone.
- Look at each image at full size, light and dark, before reporting.

## Dark theme

- Redefine every color token, not only the background. A card that keeps its light fill on a dark sheet is the usual miss.
- Raise the accent a step in the dark theme: the same saturated blue that looks crisp on paper looks muddy on navy.
- Pure white text on dark is harsh; use the same off-white you would use for body text on the brand's dark pages.
- Check contrast of the smallest text, which is where it fails first.

## When render.py prints a WARN

| WARN | Meaning | Fix |
|---|---|---|
| `content leaves the item box: x, y` | an element extends past the item's edge, so it is clipped in the image | shorten the text, widen the box or raise the item height |
| `over 300 KB` | lossless WebP of a busy image grew large | simplify gradients and lines first; use a lossy re-encode only for the image that still exceeds the budget, and say so |
