---
name: landing-pager
description: Design and build a single-file landing page (index.html) for a repository, to be served by GitHub Pages, with a look drawn from the project's own brand. Use whenever the user wants a landing page, homepage, project website, "GitHub Pages site", product page or marketing page for a repo, or wants the README turned into a web page, even if they do not say "landing". Detects an existing landing page or docs site first and stops instead of overwriting it.
---

# Landing pager

A landing page answers one question for a stranger in a few seconds: what is this, and should I try it. The README answers it for someone already inside GitHub; the landing page answers it for everyone else, so it is shorter, more visual and has one clear next step.

The structure and the look are yours to invent from the project. A tool for sleepy eyes and a CLI for infrastructure should not share a layout. What is fixed is the quality floor in `references/page-craft.md`, and the steps below that keep you from overwriting someone's site.

## Workflow

1. **Look for an existing landing page, then ask once.** Run the checks in `references/existing-landing.md`. If anything counts as one, stop, show the evidence (file paths, quoted lines) and ask whether to do nothing, build somewhere else, or replace it. Stop even when the user named `index.html` explicitly: they may not know a site already exists. If nothing exists, the same message carries the placement question below. A wrong guess here costs the user a live site, so ask rather than infer.
2. **Placement.** Propose the repository root if nothing occupies it and `docs/` if the root is taken (an app's own `index.html` is not a landing page, and overwriting it breaks the app). Say what the user must switch on afterwards: Settings, Pages, source branch and folder. You cannot change that setting from here. When the repo already deploys Pages through Actions, a hand-written page does not simply coexist: see `references/pages-setup.md` and ask.
3. **Learn the project, its brand and its rules.** Read the README, the banner or logo, existing images, colors and fonts, and the kind of project it is. Read `AGENTS.md`, `CONTRIBUTING.md` and any tests that read documentation: their rules apply to the words on the page (a ban on stating counts, on typographic dashes, on naming internal files). Ask a few labelled questions (grouped by topic, options with a recommended default) about what the repo cannot tell you: who the visitor is, the one action you want, the tone, what must not be claimed. Do not ask what is visible in the repo.
4. **Offer two or three directions before building one.** Make each a short, rough page in a scratch folder outside the repo, each with a different idea of layout, motion and mood, and look at each with `scripts/shoot.py check <root> --widths 1280 --schemes light`. Show them and let the user choose or mix. If the user says to just go ahead, pick the strongest yourself and say why.
5. **Build the chosen page as one `index.html`.** Inline CSS and JS, images in the repo's assets folder. Reuse the repo's existing illustrations when there are any (see the mobile note in `page-craft.md`); if there are none and the `illustration-render` skill is available, use it for figures, otherwise draw them in HTML and CSS. Follow `references/page-craft.md`.
6. **Make the social preview.** A 1200x630 PNG from a small HTML page kept beside the repo's other illustration sources (`assets/source/og.html` or equivalent), rendered with `shoot.py og`, referenced from the Open Graph and Twitter tags.
7. **Verify.** Run what `references/verify.md` lists: `shoot.py check` with `--axe`, then `lighthouse.py` for mobile and desktop. Fix every FAIL; report the four scores as a range with what you did about anything below 90. Look at the screenshots.
8. **Report and stop.** List the files written, the Pages setting the user must change, the checks that passed, and what was not observed: the page on the real Pages URL, the social preview in a real share card, external links. Do not commit or push unless asked.

## When no user can answer

Where a step says to ask and wait, and nobody can answer (an automated run, a test), do not stop and do not guess silently: take the recommended default, write each question with the answer you assumed to a `questions.md` the user will see, and carry on. The one exception is step 1: if an existing landing page was found, stop and write the question, because proceeding is the damage you are avoiding.

## Defaults the user has already chosen

These are starting points; ask again only if the project makes one a bad fit.

- Interactivity: a copy button for the install or usage command, a light/dark toggle that starts from the visitor's system setting, tabs where a choice of cases helps, and scroll-triggered motion that respects `prefers-reduced-motion`.
- Fonts: Google Fonts, loaded without blocking render (see `page-craft.md`). Mention once that each visitor's browser requests Google; the user accepted this.
- Metadata: title, description, Open Graph and Twitter tags, favicon, preview image. No analytics, no cookies, no third-party scripts.
- Language: the language of the project's README unless told otherwise.
