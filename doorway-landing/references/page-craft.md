# Craft floor for the page

Structure, wording and visual language are your choice and should come from the project. This file lists what any page must meet, with the reason, so you can bend a rule knowingly.

## Content judgment

- One promise above the fold, in the project's own voice, then one action. A second competing button dilutes both.
- Show the product working before explaining it: a screenshot, a figure, a short demo of the output. Claims without a picture read as marketing.
- Say who it is for and what it costs the visitor (time, money, an account). Hiding the cost makes people leave late instead of early.
- Take claims only from the README and the code. A landing page is where an invented benefit gets in.
- End with the same action as the top, plus where to read more (the README, docs).

## Build

- One file `index.html`: CSS in a `<style>`, JS in a `<script>` at the end. A single file is easy to copy, review and host.
- Semantic landmarks (`header`, `main`, `section` with headings in order, `footer`), a single `h1`, a `lang` on `html`, a viewport meta.
- Relative URLs only (see `pages-setup.md`).
- Mobile first: no horizontal scroll at 390 px, tap targets at least 44 px, line length under about 75 characters.
- Contrast of text at least 4.5:1 in both themes, checked, not guessed.
- Images carry `alt`, `width` and `height` (prevents layout jump), and `loading="lazy"` below the fold.
- Illustrations built for a README are about 2400 px wide with 17 px text; scaled to 390 px they are unreadable. Show each in a scrollable frame (`overflow-x: auto`, `tabindex="0"`, an accessible label) with the image keeping a minimum width of about 760 px, or rebuild that figure as HTML. Do not shrink it to fit.
- Words on the page obey the repo's own documentation rules: if the repo bans stating counts (skills, commands, files), that includes headings like "Eleven you call"; if it bans typographic dashes, the page does too.

## Theme

Start from `prefers-color-scheme` (a visitor with JS off gets the light theme unless the CSS says otherwise; choose deliberately); the toggle overrides it and remembers the choice in `localStorage`, inside a try/catch because storage can be blocked. Set the theme in a tiny inline script in `<head>` so the page does not flash the wrong colors.

## Motion

Scroll-triggered reveals use `IntersectionObserver` and a CSS class. Respect `@media (prefers-reduced-motion: reduce)`: with it, content is visible immediately and nothing moves. Content must be visible if JS fails: add the hidden initial state only after the script has run (a `js` class on `html`), never in the base CSS.

## Interactivity

- Copy button: `navigator.clipboard.writeText`, with a fallback that selects the text, and a visible confirmation that is also announced (`aria-live="polite"`). Never copy something the visitor cannot see.
- Tabs: real buttons with `role="tab"`, arrow-key support and `aria-selected`; panels remain readable without JS in order.
- Toggle: a `button` with an accessible name and `aria-pressed`.

## Metadata

`title`, `meta name=description`, `og:title`, `og:description`, `og:type`, `og:url`, `og:image` (absolute URL, 1200x630 PNG), `twitter:card=summary_large_image`, `rel=icon` (SVG or PNG derived from the project's logo), `theme-color` for both schemes. No analytics.

## Fonts

Take the project's fonts if it has them. Request only the weights used.

A normal `<link rel="stylesheet">` to Google Fonts blocks first paint; measured, that cost about 7 Lighthouse performance points. Load it without blocking:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="FONT_CSS_URL" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="FONT_CSS_URL"></noscript>
```

with `display=swap` in the URL. The fallback stack should resemble the real font, but exact metric matching (`size-adjust`, `ascent-override`) needs numbers you can only get from the font files; use them if you can measure them, otherwise use a plain system stack and accept a small shift rather than inventing values.

## What to avoid

- Stock photography, fake testimonials, invented numbers, counters that count up to a made-up figure.
- A hero that needs a video to make sense.
- Anything that needs a build step: the page must work when the file is opened from the folder.
