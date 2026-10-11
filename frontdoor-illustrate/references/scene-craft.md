# Scene craft

Techniques for pictures that tell a story. Shapes, colors and typefaces come from the signature (`signature.md`); this file says how to build them, not how they look.

## Choosing a scene or a diagram

- A scene earns its place when the reader should feel or grasp an idea: a before and after, a transformation, a place the project lives in. It answers "what is this like?".
- A diagram earns its place when relations or order must be exact: steps, gates, branches, a dependency. It answers "what happens, in what order?".
- When both help, make the scene the main picture and put the diagram under `<details><summary>` below it, so the precise version is there for the reader who wants it.

## Building a scene

- Draw one inline SVG per `.item`, sized to the item with a `viewBox` of 1200 by the item's height. Put headings and short tags in HTML on top, so the typeface and its rendering stay under the page's CSS.
- Work in layers: a backdrop shape, the ground, the main objects, then small details that make it feel lived in. Flat fills carry most of it. Use a gradient only where light matters: gradients make lossless WebP files several times larger.
- Define a shape used more than once in `<defs>` and place it with `<use>`, so an edit changes every copy.
- Color through the theme tokens so both themes come from one drawing. A picture drawn inside the scene that depicts a light picture and a dark picture side by side uses fixed colors, because tokens would make both identical.
- A small script is better than dozens of hand-typed bars for text-like lines; give it a fixed seed so every render is the same.
- Motion on a still image: dotted trails (`stroke-dasharray` with round caps), a slight rotation of a group (2 to 14 degrees), an offset duplicate in the shadow token under an object.
- Tell the story left to right, before to after. Label it with a few short tags, and take each word from the README or the code.

## Building a diagram

- Place cards absolutely over one SVG of connectors drawn as `M`, `H` and `V` paths, with arrowheads from a `<marker>` defined once in a hidden SVG at the top of the page (markers resolve across the SVGs of one page).
- Route an elbow through the gap between rows when a row wraps. Put a branch label on the line it names.
- Keep one idea per figure and, as a guide, no more than eleven nodes; split a larger flow into two figures.

## Checking

- `render.py` warns when content leaves the item box. Look at every image in both themes, at full size.
- A glyph drawn with a dark token vanishes on a dark ground. Give each kind of mark its own token and set it in both themes.
- Compute the contrast of the smallest text pairs instead of judging them by eye.
