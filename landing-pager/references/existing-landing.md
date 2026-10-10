# Does the repository already have a landing page?

Check all of these, read-only, before proposing anything. Any one counts.

| Check | How | What it means |
|---|---|---|
| A Pages deploy workflow | `grep -rlE "deploy-pages\|upload-pages-artifact\|peaceiris/actions-gh-pages" .github/workflows` | a site is already published, even if its source is a docs generator |
| A docs site folder | `docs-site/`, `website/`, `site/`, `docs/` with `astro.config.*`, `docusaurus.config.*`, `mkdocs.yml`, `.vitepress/`, `_config.yml` | a site generator owns the public page |
| A static page in `docs/` | `docs/index.html` or `docs/index.md` meant for the public | already publishable from `/docs` |
| A custom domain | a `CNAME` file | someone set up a public address |
| A root `index.html` with real content | open it: a heading, copy, links = landing page. A single mount point such as `<div id="app">` plus a module script = an application entry, not a landing page | the second kind must not be overwritten, and it also means the root is taken |
| The repository homepage field | `gh repo view --json homepageUrl` when `gh` is installed and `origin` is on GitHub; otherwise skip it and say it was skipped | a site the owner already advertises |

Report the evidence as paths and quoted lines, say which of the three outcomes it points to (none exists, one exists, the root is taken by an app), and let the user decide. A docs site generated from the project's docs is a landing page for this purpose even if it is plain; replacing it is a different task from creating one.
