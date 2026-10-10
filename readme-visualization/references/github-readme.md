# What a GitHub README allows

Read this before writing the markup. These are platform facts from building a real README; anything not marked verified was not tested on github.com from here.

## Allowed and not

| Works | Does not |
|---|---|
| `<picture>`, `<source media="(prefers-color-scheme: dark)">`, `<img>` with `width`/`height`/`alt` | CSS, `<style>`, JavaScript, iframes, `onclick` |
| `<details><summary>`, `<p align="center">`, tables, fenced code, Mermaid | an image map: one image is one link, so a row of buttons is a row of images |
| WebP and PNG images in the repo, relative paths | SVG text in a custom web font: an SVG used through `<img>` does not load fonts, so text falls back |

## Light and dark images

```html
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/x-dark.webp"><img src="assets/x.webp" alt="..." width="100%"></picture>
```

The light file is the `<img>` fallback, so a viewer that ignores `<picture>` still gets an image. A linked image wraps the whole `<picture>` in `<a href="#anchor">`. A banner that is multiplied onto a white ground has no dark version; leave it as one light image.

## Navigation row

A row of image buttons under the banner, each `<a href="#section"><picture>...<img height="34"></picture></a>` inside `<p align="center">`. Anchors are the lowercase, hyphenated heading text. Check that every target heading exists after the rewrite, and that an external link (a guide page, a docs site) is a full URL.

## Alt text

An image is invisible to search, to screen readers and to anyone with images off. The alt text is the text form of the figure: for a diagram, narrate every node and every edge in order; for a card or button, say what it says. When a Mermaid or text form of a diagram is removed to make room for the image, the alt text and any neighboring table become the only text form, and that cost belongs in the plan the user approves.

## Layout habits that held up

- Lead with the banner, one bold sentence, then the navigation row, then the problem figure.
- Keep install commands, command tables and anything copyable as text.
- Put long reference material (contracts, writing policy, compatibility notes) under one `Reference` heading at the end so the visual sections stay short.
- Move secondary tables and directory trees into `<details>`, keeping the summary line informative.
- One figure per idea, with at most two sentences of text beside it.
- Image widths: `width="100%"` for wide figures; `height="34"` for buttons.

## Sizes

Budget about 300 KB per image and a few MB for the whole set; every re-render adds its size to git history again, so settle the design before the final render.
