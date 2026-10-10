# Serving index.html with GitHub Pages

The skill writes files; it cannot switch on Pages, and it never pushes.

## Where the file can live

| Location | Pages setting the user needs | Use when |
|---|---|---|
| `index.html` at the repository root | Settings > Pages > Deploy from a branch > the branch > `/ (root)` | nothing else occupies the root |
| `docs/index.html` | the same, folder `/docs` | the root holds an application's own `index.html`, or the repo prefers docs in `docs/` |
| anywhere, with a workflow | Settings > Pages > Source: GitHub Actions | the repo already deploys through an Actions workflow; adding a second source would conflict, so ask |

Jekyll runs on branch deploys. An `index.html` with no front matter is served as is, but files and folders starting with an underscore are ignored unless a `.nojekyll` file sits beside the page. Add `.nojekyll` only when the page folder needs such a path, and say that you did.

## When the repository already deploys through Actions

If a workflow uploads a Pages artifact (a docs generator's `dist/`), the Pages source is "GitHub Actions" and a static `index.html` in the repository root is never served. A hand-written page can only join that site by changing the workflow (copying the file into the artifact) or by living where the generator publishes static files (for example its `public/` folder). Both change what is already deployed, so do not do either without the user saying so; show the options and let them pick, and mention that editing the workflow is a change to their deploy.

## Paths

A project site lives at `https://<owner>.github.io/<repo>/`, not at the domain root. Write every URL in the page as relative (`assets/hero.webp`, not `/assets/hero.webp`), including the Open Graph image, where the full absolute URL is required: build it from `https://<owner>.github.io/<repo>/assets/og.png` and tell the user it only resolves after Pages is on.

## What to tell the user afterward

1. Which setting to change and to what.
2. The URL the page will appear at, and that the first deploy can take a minute or two.
3. That the Open Graph image only shows in a share card after the page is live; sharing debuggers cache it, so re-scrape after changes.
