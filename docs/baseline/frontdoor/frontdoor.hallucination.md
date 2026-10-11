---
baseline_schema: "2.0"
pack: "frontdoor"
document: "hallucination"
status: "active"
updated: "2026-10-11"
code_ref: "uncommitted"
---

# Frontdoor: Decisions and Open Questions

## Entry index

One row per entry. A row states what the entry is about and nothing more. An answer that turns on an entry whose full text was not read is unbacked.

| Entry | About | Status | Related |
|---|---|---|---|
| FD-D1 | splitting the work into three skills | current | FD-D2 |
| FD-D2 | how self-contained each skill is (its placement was reversed by FD-D13) | current | FD-D1, FD-D13 |
| FD-D3 | how an illustration is produced: HTML source, WebP pair, finishing step | current | FD-D4, FD-D5 |
| FD-D4 | which browser takes the screenshots | current | FD-D3, FD-D8 |
| FD-D5 | whether the skills fix a visual style | current | FD-D3 |
| FD-D6 | what `frontdoor-landing` does when a landing page may already exist | current | FD-D9 |
| FD-D7 | the quality floor every generated landing page must meet | current | FD-D8, FD-D12 |
| FD-D8 | how a landing page is verified, with scripts shipped in the skill | current | FD-D4, FD-D7 |
| FD-D9 | what a skill does when nobody can answer its questions | current | FD-D6 |
| FD-D10 | why there is no `useguide` in this pack | current | none |
| FD-D11 | a review page that showed raw markup instead of results | current, lesson | FD-D12 |
| FD-D12 | a generated page that broke a rule it had read about | current, lesson | FD-D7 |
| FD-D13 | where the skills live: repository root, installable one folder at a time | current | FD-D2, FD-Q1 |
| FD-D14 | the repository and skill names: `frontdoor` prefix, short verbs | current | FD-D13, FD-Q1 |
| FD-Q1 | whether the skill descriptions make a host select the skills correctly | open | none |
| FD-Q2 | whether the skills need automated tests | open | none |
| FD-Q3 | whether the scripts work on macOS and Linux | open | FD-D8 |

## FD-D1: three skills, not one

Decision: keep planning a README, rendering illustrations and building a landing page as three skills - they trigger on different requests and the render step is reused by the other two.

What breaks if ignored: one large skill loads render instructions for every README question and cannot be copied without the landing page.

Rejected: two skills (planning plus landing, render alone) - the landing page uses its own checks and shares no files with README planning.

Rejected: one skill with subfolders - description text has to cover three unrelated trigger phrases, which weakens selection.

## FD-D2: self-contained skills, siblings optional

Decision: let each skill carry every script and reference it runs; a skill names a sibling only as optional help - a folder installed into another repository must work alone. Where the folders sit is FD-D13; this entry first placed them in `.claude/skills/<name>/`, which FD-D13 reversed.

What breaks if ignored: a skill that requires a sibling's file fails in the repository it was installed into, after the user has already asked for something.

Rejected: one shared scripts folder - installing one skill would drop the scripts it calls.

## FD-D3: an illustration is an HTML block rendered to a WebP pair

Decision: build each image as a `.item` in an HTML page, screenshot it at 2x, round the corners and draw the border with `render.py`, and save lossless WebP as `<id>.webp` and `<id>-dark.webp` - the brand's real fonts survive, one source gives both themes, and a later edit is a text edit plus one command.

What breaks if ignored: images made by hand drift from each other and cannot be regenerated; the dark image is not a recolor of the light one.

Measured: a set of 17 images in both themes built this way came to about 3.7 MB, each file under 300 KB; the 300 KB budget is a default of `render.py`, which warns above it.

Rejected: SVG - an SVG loaded through `<img>` does not load web fonts, so text falls back (platform behaviour, not tested here).

Rejected: PNG output - larger for the same pixels; the PNG size was not measured.

Rejected: a single light image with a border - the user wanted a dark variant of every image.

Rejected: Mermaid for diagrams - no control over fonts, spacing or the dark theme.

## FD-D4: screenshots come from the Edge or Chrome already installed

Decision: drive the installed browser through Playwright's channel option (Edge, then Chrome, then Playwright's own build) - nothing is downloaded and no administrator rights are needed.

What breaks if ignored: a skill that downloads a browser fails on a locked-down machine, or needs a setup step before the first image.

Rejected: a browser MCP server for the screenshots - the one available while building could write only inside the repository root, which forced intermediate files into the repository.

Rejected: requiring `playwright install` - a multi-hundred-megabyte download the user did not ask for.

## FD-D5: the skills fix a contract, not a style

Decision: `frontdoor-illustrate` ships a starter whose colors and fonts are placeholders and states the contract a source page must meet (a unique id per `.item`, 2x zoom, theming through `html[data-theme]`, a border-color token) - brand evidence comes from the target repository, and a skill asks the user for a direction only when the repository has none.

What breaks if ignored: every repository ends up with the same palette, and a fixed palette is replaced in full on first use.

Rejected: shipping one house style - the user stated that each brand has its own identity.

Rejected: strict structure for the landing page - the user wanted the agent free to invent layout and content; only the quality floor in FD-D7 is fixed.

## FD-D6: stop when a landing page may exist, and ask before writing

Decision: `frontdoor-landing` runs a read-only check (Pages deploy workflow, docs-site generator folder, `docs/index.*`, `CNAME`, a root `index.html` with real content, the homepage field when `gh` is available), stops with the evidence if anything counts, and asks where `index.html` goes before writing - an overwritten page is a live site lost.

What breaks if ignored: the skill replaces an application's own `index.html` or adds a page that the deploy never serves.

Observed: on an app repository the check found a Pages deploy through Actions, an Astro docs site, a splash home page in `docs/index.md` and a root `index.html` that was the app's settings window entry; the runs with and without the skill both stopped, so this scenario did not separate the two.

Rejected: building anyway at a different path - the user may want the existing site left alone, which only they can say.

Rejected: treating only a Pages workflow or a `CNAME` as proof - a generator-based docs site counts as a landing page.

## FD-D7: the quality floor for a generated landing page

Decision: one `index.html` with inline CSS and JS; relative URLs except the absolute Open Graph image; light/dark from the system setting with a stored override; motion that respects reduced motion and content visible without JS; a copy button, tabs and a toggle that work by keyboard; title, description, Open Graph, Twitter, favicon and a 1200x630 preview PNG; no analytics; Google Fonts loaded without blocking first paint, using `rel=preload` with an `onload` swap and a `noscript` fallback.

What breaks if ignored: a page that needs scripts to show content, flashes the wrong theme, or blocks first paint on a font host.

Measured: in one trial run a normal font stylesheet link cost about 7 Lighthouse performance points on the mobile profile; the preload pattern recovered them. A single run, not repeated.

Accepted cost: each visitor's browser requests Google Fonts; the user accepted this.

Rejected: a build step or framework - the page must work when the file is opened from its folder.

Rejected: matching fallback-font metrics with invented `size-adjust` numbers - without measuring the font files the numbers would be made up; a plain system stack and a small layout shift are accepted instead.

## FD-D8: verification scripts ship inside the skill

Decision: `frontdoor-landing` carries `shoot.py` (three widths, light and dark, reduced motion, broken links and images, metadata, preview size, optional axe-core) and `lighthouse.py` (serves the folder, starts Edge or Chrome with a debugging port, runs Lighthouse through `npx`, prints the four scores and the audits that lost points) - Lighthouse run alone audits only the scheme the page starts in, and its own launch of Edge failed in a trial run.

What breaks if ignored: a dark-theme contrast failure ships unseen (it was found in the trial only by injecting axe-core under the dark scheme); the documented Lighthouse command fails on Windows.

Observed: `lighthouse.py` returned 100, 100, 100, 100 for two trial pages; trial runs of the same pages by hand ranged from 84 to 99 on performance, so a single score is not a result and the skill says to run twice and report the range.

Rejected: telling the agent to run the Lighthouse command by hand - the command from the first draft failed in the trial and the working procedure needs several steps.

Rejected: bundling axe-core - a 650 KB file; it already ships inside the Lighthouse install that `npx` fetches.

## FD-D9: with nobody to ask, take the default and write the questions down

Decision: where a skill says to ask and wait and no one can answer (an automated run), take the recommended default, write each question with the assumed answer to a `questions.md`, and continue - except that when an existing landing page is found the skill stops, because continuing is the damage the check exists to prevent.

What breaks if ignored: an unattended run either stalls or guesses silently; the second is invisible to the user.

Rejected: always stopping at the first question - no useful work gets done unattended and the trial could not exercise the build steps.

## FD-D10: no `useguide` document in this pack

Decision: omit `useguide` - the consumer contract of each skill is its own `SKILL.md`, and a second description in a pack would drift from it.

What breaks if ignored: two descriptions of how to invoke a skill, one of them never read by the agent that runs it.

## FD-D11: a review page that showed raw markup instead of results

What was believed: the skill-creator's static review viewer could show every run's output folder.

What disproved it: the viewer embedded each output file as text. The folder held a landing page (HTML), Lighthouse reports (JSON) and a 650 KB script, so the page showed `\n` sequences, raw JSON, an empty prompt and "No output files found".

Why it looked reasonable: the viewer is the documented way to review runs, and the files were exactly what the user should see.

Fix: build a plain comparison page of screenshots and images side by side from copies kept in a separate folder, and keep raw reports out of the folders a viewer scans.

## FD-D12: a generated page broke a rule it had read about

What was believed: the with-skill landing page avoided stating counts, as its repository forbids; the agent reported that no skill count appeared in prose.

What disproved it: a heading read "Eleven you call", a count of skills. A search of the other page found none.

Why it looked reasonable: the agent searched for counts in body text and treated headings as labels.

Fix: `frontdoor-landing` step 3 now says to read the repository's contributor rules and tests before writing words, and `page-craft.md` names headings as covered. The fix was not re-run.

## FD-D13: skills at the repository root, one installable folder each

Decision: keep each skill at the repository root as `<name>/` holding `SKILL.md`, `agents/openai.yaml` and its own `scripts/`, `assets/`, `references/` - the layout `npx skills add <repository> --skill <name>` installs one folder at a time; `allow_implicit_invocation` is `true` in each `openai.yaml` because the skills should be chosen from a plain request (FD-Q1). Supersedes the placement in FD-D2.

What breaks if ignored: the user asked for the npx-installable format; a folder under `.claude/skills/` serves only a person copying it by hand into another repository.

Observed 2026-10-11 against the pushed repository: `npx skills add <repository> --list` found all three skills, and a single-skill install of the illustration skill into an empty repository installed all seven files of that skill, scripts and assets included, under `.claude/skills/<skill>/`.

Not verified: installing the other two skills, other agents, whether `npx skills add` also discovers skills under `.claude/skills/`, and whether any host other than Codex reads `agents/openai.yaml`; the file is a display and policy hint, and a skill works without it.

Rejected: keeping `.claude/skills/` - it was the first layout (FD-D2) and the user replaced it.

Rejected: a `skills/` parent folder - no reason was given to add a level, and the root layout is what the user named.

## FD-D14: the repository and the skills are named `frontdoor`

Decision: name the repository `frontdoor` and the skills `frontdoor-readme`, `frontdoor-illustrate` and `frontdoor-landing` - a repository's front door is its README and landing page, and a prefix groups the three when listed; the folder, the `name` frontmatter, `agents/openai.yaml` and the README commands use the same string.

What breaks if ignored: a folder name that differs from its `name` frontmatter, or an install command that names a skill or repository that does not exist, makes `npx skills add <repository> --skill <name>` find nothing.

Observed 2026-10-11 against the published repository: `npx skills add https://github.com/the-khiem7/frontdoor.git --list` found all three skills, and a global install of all three for Claude Code and Gemini CLI placed each under `~/.agents/skills/`, linked it from `~/.claude/skills/`, and recorded the GitHub repository as its source.

Not verified: whether the short verbs weaken host selection (FD-Q1), an install on another operating system (FD-Q3), and an install into a project rather than globally.

Rejected: the long names (`frontdoor-readme-visualization`, `frontdoor-illustration-render`, `frontdoor-landing-pager`) - the user chose short names.

Rejected: a suffix (`landing-frontdoor`) - the user chose the prefix form.

Rejected: a company brand such as STYL as the prefix - the user wanted the repository's own name.

Rejected: `doorpaint` - a search for it also returns paint for physical doors.

Rejected: `storefront`, `easel`, `mural`, `atelier`, `gesso`, `varnish`, `palette`, `fresco`, `curb-appeal`, `facade`, `porch`, `lobby`, `repo-polish` - offered, not chosen.

## Open questions

### FD-Q1: do the skill descriptions make a host pick the skills on a plain request?

Selection was tested only by giving a subagent the skill path. The descriptions were written to be assertive and the optimizer in the skill-creator plugin was not run. What is at stake: a skill that is never selected is dead weight. Trigger to reopen: a plain request ("make the README nicer", "add a GitHub Pages site") that does not invoke the skill.

### FD-Q2: do the skills need automated tests?

Nothing checks the scripts or the skill text beyond `quick_validate` and the manual runs recorded in the roadmap. What is at stake: a later edit to `render.py`, `shoot.py` or `lighthouse.py` can break a path nobody re-runs. Trigger to reopen: the first regression, or a decision on where the skills finally live.

### FD-Q3: do the scripts work on macOS and Linux?

All runs were on Windows with Edge. `lighthouse.py` carries browser paths for macOS and Linux that were never executed, and `render.py` and `shoot.py` rely on Playwright's Edge and Chrome channels. What is at stake: a copy of the skills on another operating system fails at the first script. Trigger to reopen: a run on either system.
