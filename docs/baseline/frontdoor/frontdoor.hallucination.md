---
baseline_schema: "2.0"
pack: "frontdoor"
document: "hallucination"
status: "active"
updated: "2026-10-12"
code_ref: "uncommitted"
---

# Frontdoor: Decisions and Open Questions

## Entry index

One row per entry. A row states what the entry is about and nothing more. An answer that turns on an entry whose full text was not read is unbacked.

| Entry | About | Status | Related |
|---|---|---|---|
| FD-D1 | splitting the work into three skills | current | FD-D2 |
| FD-D2 | how self-contained each skill is (its placement was reversed by FD-D13) | current | FD-D1, FD-D13, FD-D16 |
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
| FD-D15 | the README pictures; moved to the readme-design pack as RD-D1, RD-D2, RD-D3 | moved | FD-D16, RD-D1 |
| FD-D16 | how `frontdoor-readme` depends on `frontdoor-illustrate` | current | FD-D2, RD-D3, FD-Q1 |
| FD-D17 | that the skills ship no reusable look and each repository gets its own signature | current | FD-D5, RD-D2 |
| FD-D18 | that every run ends with a hero banner, in a greenfield and in a brownfield repository | current | FD-D17 |
| FD-D19 | that `frontdoor-readme` writes the complete README, with every statement traced to the repository | current | FD-D18 |
| FD-D20 | how a README chooses between a scene, a diagram and `<details>` | current | RD-D3, FD-D17 |
| FD-D21 | the three tiers of skill rules and what `render.py` reports about fonts and the starter | current | FD-D3, FD-D17 |
| FD-D22 | that `signature.md` is shipped as three byte-identical copies | current | FD-D2, FD-D17 |
| FD-D23 | examples in `signature.md` that anchored a trial agent toward a copy | current, lesson | FD-D17, FD-D22 |
| FD-D24 | where rough design directions are shown: one local board per repository, every round on it | current | FD-D2, FD-D9, FD-D22, FD-Q3 |
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

## FD-D15: the README pictures, moved to the readme-design pack

Moved to the `readme-design` pack as RD-D1 (how the pictures are produced and where they live), RD-D2 (the look) and RD-D3 (a scene per skill, the flow inside `<details>`); the open points are RD-Q1 and RD-Q2. This number stays reserved and is not reused.

## FD-D16: `frontdoor-readme` uses `frontdoor-illustrate` only when it is available

Decision: step 4 of `frontdoor-readme` and its `description` hand the image build to `frontdoor-illustrate` when it is available, and tell the agent to say so and ask the user how to produce the images when it is not - a skill installed alone must still run (FD-D2), and the README and `AGENTS.md` both say siblings are optional help.

What breaks if ignored: `frontdoor-readme` installed alone reaches step 4 after the user approved the plan with no renderer and no instruction; the `skills-map` figure in the README either contradicts the skill or the README text (RD-D3, pack readme-design).

Observed: `quick_validate` reports the edited skill valid. The trigger phrases in `description` are unchanged; only its last clause was reworded (FD-Q1).

Not verified: a run of `frontdoor-readme` without `frontdoor-illustrate` installed; the skill carries no renderer of its own, so what happens after the question is the user's call.

Rejected: keep the hard hand-off, draw it as a solid arrow and reword the README - the README would then admit a skill that cannot run alone.

Rejected: draw no arrows between skills and log the mismatch as an open question - the skill text was fixable in one clause.

## FD-D17: no reusable look is shipped; each repository gets its own signature

Decision: ship no reusable look: the starter of `frontdoor-illustrate` carries only the renderer contract and theme tokens marked `STARTER-PLACEHOLDER`, and `references/signature.md` makes the agent derive, per repository, a signature of vector shape language, typeface and presentation - several projects that use the skills must not end up with one design and different text. This hardens FD-D5.

What breaks if ignored: a starter with components (cards, chips, arrows, rings, lanes) is the look every repository starts from and keeps; this repository's own look (an arched doorway, amber, Fraunces, DM Sans, JetBrains Mono; RD-D2) copied as a template does the same.

Rejected: a gallery of ready styles to pick from - the choice ranges over a fixed set, so outputs converge.

Rejected: a detailed design rulebook - it limits the creativity this family exists for.

Rejected: keeping the starter components as optional - an agent uses what is on the shelf.

## FD-D18: every run ends with a hero banner

Decision: end every `frontdoor-readme` run with a hero banner, in a greenfield and in a brownfield repository; a greenfield repository is one with no README or only a draft and no brand evidence (banner, logo, CSS, docs site), and there the signature is invented from the subject, while an existing banner in a brownfield repository is assessed against the repository's signature, kept when it fits, and replaced only by a proposal the user approves when it does not (low resolution, no dark version, off-brand) - a README with no front picture leaves the first 30 seconds to plain text.

What breaks if ignored: a README without a hero reads like every other one; always making a new hero overwrites a brand someone chose.

Rejected: a hero only for greenfield repositories - the user wants it in every run.

Rejected: always a new hero whatever exists - it would replace a banner that already fits.

## FD-D19: `frontdoor-readme` writes the complete README

Decision: have `frontdoor-readme` write the complete README, not a skeleton, tracing every sentence and command to code, configuration, existing docs or an answer from the user, and asking about what it cannot trace instead of guessing - the target of the workflow is a finished page. This widens the scope in the introduction, which had left the project's own documentation out.

What breaks if ignored: an invented feature or an install command written from memory reaches the page every visitor reads first; a skeleton leaves the user the part that makes the page worth reading.

Rejected: a skeleton README with placeholders - the user wants the finished page.

Rejected: stopping until the user writes the README - it defeats the greenfield case.

## FD-D20: a scene first, a diagram where it fits, `<details>` for the secondary

Decision: prefer a vector scene when the reader should feel or grasp an idea, use a diagram when relations or order must be exact, use both when each helps (the scene as the main figure, the diagram inside `<details>`), and put secondary material (step-by-step flows, secondary tables, trees, status) under `<details><summary>` but never the install commands - the user found step boxes heavy and wants pictures that reach the reader (RD-D3).

What breaks if ignored: a reader meets a wall of step boxes first; a hidden install command costs the one action most visitors came for.

Rejected: a fixed table of content type to figure type (the old `audit-and-plan.md` table) - it pushes every repository toward the same figures.

Rejected: diagrams only - they carry the order but not the feeling.

## FD-D21: three tiers of rules, and `render.py` reports fallback fonts and a leftover starter

Decision: write each rule of the skills at one of three tiers - the renderer contract (hard), a quality floor of legibility, measured contrast, truthful pictures and no skill counts (hard, each with its reason), and design (free, drawn from the repository) - and have `render.py` print a WARN, counted toward exit 1, when a font family was requested but not loaded and when a served stylesheet still holds `STARTER-PLACEHOLDER`, because the agent cannot see either from the image.

What breaks if ignored: a fallback face lands in every image with no signal, which defeats a typeface chosen to be distinctive (RD-D1); a rule with no tier is applied as a design rule and narrows the result.

Rejected: one flat list of rules - an agent cannot tell a hard constraint from a taste.

Rejected: a lint of the colors and shapes against a style guide - it would be a rulebook by another name (FD-D17).

## FD-D22: `signature.md` is shipped as three byte-identical copies

Decision: put the same `references/signature.md` in `frontdoor-illustrate`, `frontdoor-readme` and `frontdoor-landing`, and compare the copies with `cmp` - a skill installed alone must still carry the method (FD-D2).

What breaks if ignored: a copy edited alone makes the skills teach different methods, and nothing else compares them.

Rejected: one copy in `frontdoor-illustrate` with the other two pointing to it - a lone `frontdoor-readme` or `frontdoor-landing` would have no method.

## FD-D23: examples in `signature.md` anchored the agents they were meant to free

What was believed: a table of worked signatures for ordinary subjects (an infrastructure audit tool, a children's reading app) shows the method without being copied, because the file says never to choose from it.

What disproved it: in the two-repository trial, the agent working on a children's story app wrote that its first direction came close to the "cut-paper collage" row for a children's reading app and had to steer away on purpose, and the agent working on an infrastructure audit tool had to avoid the "survey-map blueprint" row for the same reason. The `pebble` run also chose Fraunces, the display face of this repository's own look.

Why it looked reasonable: the rows were labelled as illustrations of the method, and the file forbids copying.

Fix: the rows now use unusual subjects (subtitle parser, secret rotator, tiny-language compiler, ferry timetable, photo renamer, fuzzer), the file says a project of the same kind as an example must still derive its own, and the defaults list names the display faces agents reach for first (Fraunces, Playfair Display, Space Grotesk, Inter). The second trial that would confirm this was not run.

## FD-D24: rough directions go on one local board per repository, every round on it

Decision: show every round of rough directions on one local page, `.frontdoor/directions.html` in the repository being worked on, built by `scripts/board.py` (standard library only) from `.frontdoor/directions.json`; each round is appended and the newest is shown first, the round's sources and renders live under `.frontdoor/round-<N>/`, and the script adds `.frontdoor/` to `.gitignore` - the sketches are scratch, a design can take many rounds, and the user opens one file with a double click. The method is the "Show the directions" section of `signature.md`; `board.py` ships as three byte-identical copies, one per skill, compared with `cmp` like `signature.md` (FD-D22).

What breaks if ignored: a hosted page per round (a published Claude artifact was used in the first run on the `ghist` repository) piles scratch pages up in the user's account and may expose unreleased work; a list of scratch paths makes the user open each sketch by hand; one board per round makes rounds impossible to compare.

Observed 2026-10-12 on Windows with Edge, against a throwaway repository and against `ghist` with two rounds of three directions: a round is appended and the ids continue across rounds; `choose` records the pick; a missing image file, a path outside the folder, an unknown direction id and an id used twice each stop with exit 1 and write nothing; `.frontdoor/` is added to `.gitignore` and `git status` no longer lists it; the board showed no horizontal overflow at 1200 px light and 400 px dark; the page linking its images was 4.9 KB and `--inline` made 210 KB for the same four images.

Not verified: the `open` and `xdg-open` calls on macOS and Linux (FD-Q3); the window opened on Windows was not observed, only that `os.startfile` returned; the board in Firefox or Safari; a full run of any skill that follows the new text.

Rejected: a published Claude artifact per round - one page per round accumulates in the user's gallery for scratch work.

Rejected: a scratch folder outside the repository (the previous wording of the three `SKILL.md` files) - the user wants the board kept with the repository that runs the skills, ignored by git.

Rejected: a new board file per round - older rounds drop out of view and cannot be compared.

Rejected: images embedded by default - the file grows by every image of every round; `--inline` exists for the one file that must be sent.

Rejected: the rule in prose only, with no script - every run would rewrite the page and the layouts would differ.

Rejected: `board.py` in `frontdoor-illustrate` only - a `frontdoor-readme` or `frontdoor-landing` installed alone would have no board (FD-D2).

## Open questions

### FD-Q1: do the skill descriptions make a host pick the skills on a plain request?

Selection was tested only by giving a subagent the skill path. The descriptions were written to be assertive and the optimizer in the skill-creator plugin was not run. What is at stake: a skill that is never selected is dead weight. Trigger to reopen: a plain request ("make the README nicer", "add a GitHub Pages site") that does not invoke the skill.

### FD-Q2: do the skills need automated tests?

Nothing checks the scripts or the skill text beyond `quick_validate` and the manual runs recorded in the roadmap. What is at stake: a later edit to `render.py`, `shoot.py` or `lighthouse.py` can break a path nobody re-runs. Trigger to reopen: the first regression, or a decision on where the skills finally live.

### FD-Q3: do the scripts work on macOS and Linux?

All runs were on Windows with Edge. `lighthouse.py` carries browser paths for macOS and Linux that were never executed, and `render.py` and `shoot.py` rely on Playwright's Edge and Chrome channels. What is at stake: a copy of the skills on another operating system fails at the first script. Trigger to reopen: a run on either system.
