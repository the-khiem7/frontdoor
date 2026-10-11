# What a GitHub README allows

Read this before writing the markup. These are platform facts from building a real README; anything not marked verified was not tested on github.com from here.

## Allowed and not

| Works | Does not |
|---|---|
| `<picture>`, `<source media="(prefers-color-scheme: dark)">`, `<img>` with `width`/`height`/`alt` | CSS, `<style>`, JavaScript, iframes, `onclick` |
| `<details><summary>`, `<p align="center">`, tables, fenced code, Mermaid | an image map: one image is one link, so a row of buttons is a row of images |
| WebP and PNG images in the repo, relative paths | SVG text in a custom web font: an SVG used through `<img>` does not load fonts, so text falls back |

Not yet checked on github.com: a `<picture>` inside `<details>`, a `<picture>` inside an `<h1>`, and the pictures at a phone's width. Say so in the report until someone has looked.

## Light and dark images

```html
<picture><source media="(prefers-color-scheme: dark)" srcset="assets/x-dark.webp"><img src="assets/x.webp" alt="..." width="100%"></picture>
```

The light file is the `<img>` fallback, so a viewer that ignores `<picture>` still gets an image. A linked image wraps the whole `<picture>` in `<a href="#anchor">`. A banner that is multiplied onto a white ground has no dark version; leave it as one light image.

## The hero banner

The hero goes first, before the text. Wrap it in `<h1 align="center">` when it carries the project's name, and give it alt text that starts with the name and the one-line promise, so the page still has its heading with images off, then a short description of what is drawn. Follow it with one bold sentence.

## `<details>`

Use `<details><summary>` for material most readers will not need first: a step-by-step flow under a scene, a secondary table, a directory tree, a long reference, a status note. Keep the summary line informative. Leave a blank line after `<summary>` and before `</details>`, or the markdown inside does not render. Never put the install or the first usage command inside one.

## Navigation row

Optional. A row of image buttons under the banner, each `<a href="#section"><picture>...<img height="34"></picture></a>` inside `<p align="center">`. Anchors are the lowercase, hyphenated heading text. Check that every target heading exists after the rewrite, and that an external link (a guide page, a docs site) is a full URL. A short README rarely needs one.

## Alt text

An image is invisible to search, to screen readers and to anyone with images off. The alt text is the text form of the figure: for a diagram, narrate every node and every edge in order; for a scene, describe what is drawn and read its labels; for a card or button, say what it says. When a Mermaid or text form of a diagram is removed to make room for the image, the alt text and any neighboring table become the only text form, and that cost belongs in the plan the user approves. A flow with many nodes makes a long alt text for a screen reader; when the flow sits inside `<details>`, a concise alt text plus the steps as a short list under the picture serves better.

## Layout habits that held up

Suggestions, not a template: the reader's path matters more than the order of any one README.

- A hero first, then one bold sentence, then the figure that answers "what is this?".
- Keep install commands, command tables and anything copyable as text.
- Put long reference material (contracts, writing policy, compatibility notes) under one `Reference` heading near the end so the visual sections stay short.
- One figure per idea, with at most two sentences of text beside it.
- Image widths: `width="100%"` for wide figures; `height="34"` for buttons.

## Sizes

Budget about 300 KB per image and a few MB for the whole set; every re-render adds its size to git history again, so settle the design before the final render.
