---
baseline_schema: "2.0"
pack: "frontdoor"
document: "hallucination"
status: "active"
updated: "2026-11-25"
code_ref: "uncommitted"
---

# Frontdoor: Decisions and Open Questions

## Entry index

One row per entry. A row states what the entry is about and nothing more. An answer that turns on an entry whose full text was not read is unbacked.

| Entry | About | Status | Related |
|---|---|---|---|
| FD-D1 | splitting the work into three skills | current | FD-D2 |
| FD-D2 | how self-contained each skill is (its placement was reversed by FD-D13) | reversed by FD-D36 | FD-D1, FD-D13, FD-D16, FD-D36 |
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
| FD-D18 | that every run ends with a hero banner, in a greenfield and in a brownfield repository | current, extended by FD-D32 | FD-D17, FD-D32 |
| FD-D19 | that `frontdoor-readme` writes the complete README, with every statement traced to the repository | current | FD-D18 |
| FD-D20 | how a README chooses between a scene, a diagram and `<details>` | current | RD-D3, FD-D17 |
| FD-D21 | the three tiers of skill rules and what `render.py` reports about fonts and the starter | current | FD-D3, FD-D17 |
| FD-D22 | that `signature.md` is shipped as three byte-identical copies | reversed by FD-D36 | FD-D2, FD-D17, FD-D36 |
| FD-D23 | examples in `signature.md` that anchored a trial agent toward a copy | current, lesson | FD-D17, FD-D22 |
| FD-D24 | where rough design directions are shown: one local board per repository, every round on it | amended by FD-D31; location reversed by FD-D37, copies by FD-D36 | FD-D2, FD-D9, FD-D22, FD-D31, FD-D36, FD-D37, FD-Q3 |
| FD-D25 | how a landing page uses motion, and what it does under reduced motion | current, lesson | FD-D7, FD-D8 |
| FD-D26 | the UI gallery skill; moved to the ui-gallery pack as UG-D1 | moved | UG-D1 |
| FD-D27 | the gallery page's neutral look; moved to the ui-gallery pack as UG-D2 | moved | FD-D17, UG-D2 |
| FD-D28 | where a gallery lives; moved to the ui-gallery pack as UG-D3 | moved | UG-D3 |
| FD-D29 | the stack references; moved to the ui-gallery pack as UG-D4 | moved | UG-D4 |
| FD-D30 | how a state is mocked and shot; moved to the ui-gallery pack as UG-D5 | moved | UG-D5 |
| FD-D31 | one design board per purpose: readme, landing-page, product | reversed by FD-D37 | FD-D24, FD-D22, FD-D37 |
| FD-D32 | the banner and social preview names, GitHub's social preview rules (still image only), and the optional animated README banner | current, lesson; the GIF format amended by FD-D33 | FD-D18, FD-D3, FD-D31, FD-D33 |
| FD-D33 | animated WebP as the only animated format, and the banner shown under reduced motion | current | FD-D32, FD-D34 |
| FD-D34 | how `animate.py` encodes: libwebp effort 4, worker processes, frames on disk, one run at a time | current, lesson; the encoder and the frames on disk amended by FD-D35 | FD-D33, FD-D35 |
| FD-D35 | `animate.py` encodes frame by frame in a pool and joins the WebP container itself; parallel capture, sway dedupe, `--draft`, `--batch` | current | FD-D34, FD-D33 |
| FD-D36 | a `frontdoor-core` skill that the other skills require | current, implemented in Phases 10 and 12 | FD-D2, FD-D22, FD-D24 |
| FD-D37 | one board per repository, a page per use case, rounds numbered per page | current, implemented in Phases 10 and 11 | FD-D24, FD-D31, FD-D36 |
| FD-D38 | the board's neutral look and its interface: hover table of contents, one frame per image, theme divider | current, implemented in Phase 11; layout and header amended by FD-D45 | FD-D17, FD-D37, UG-D2 |
| FD-D39 | how the user's choice returns from the board: copy button, later a local server | current, copy button implemented in Phase 11, server not built | FD-D37, FD-D38 |
| FD-D40 | asking the number of variants every round | current, implemented in Phases 10 and 12 | FD-D9, FD-D24 |
| FD-D41 | the harness language and its browser daemon | current, implemented in Phase 10 | FD-D34, FD-D35, FD-D36 |
| FD-D42 | the skills installed at project scope to help write the harness | current | FD-D41 |
| FD-D43 | why `board.html` hides with `!important`, and why a pasted choice goes to `fd choose` through a file | current, lesson | FD-D38, FD-D39 |
| FD-D44 | why `fd render` warned that a web font it had drawn was not loaded, and what the trial runs found missing in the skill text | current, lesson | FD-D36, FD-D40, FD-D41 |
| FD-D45 | the board's header, branding, card layout and floating choice controls after the user's first review | current, implemented in the Phase 11 revision | FD-D38, FD-D39, FD-D46 |
| FD-D46 | keeping the two board changes the agent made beyond the review: no chosen tag, and the per-row switch | current, implemented in the Phase 11 revision | FD-D45, FD-Q4 |
| FD-Q1 | whether the skill descriptions make a host select the skills correctly | open | none |
| FD-Q2 | whether the skills need automated tests | open | none |
| FD-Q3 | whether the scripts work on macOS and Linux | open | FD-D8 |

## FD-D46: keep the board without the chosen tag, and with the per-row switch

Decision: decided by the user on 2026-11-25. Closes FD-Q4.

- a card carries no "Chosen in the record" tag; a picked card shows its coloured border, its letter filled and its button reading Picked, and the record stays in the card's accessible name
- a 1, 2 and 3 switch in the top bar sets how many variants share a row; one is the default, the choice is remembered in the browser, and a phone always shows one

Why: the tag repeated what the border, the letter and the button already show, without the state resting on colour alone [user]. The switch keeps a side-by-side look one click away, because the Compare viewer appears only on a round whose `round.json` allows it [agent].

What breaks if ignored: a returned tag crowds the card head; without the switch, seeing every variant at once needs a round marked for comparison.

## FD-D45: the board's header, branding, card layout and floating choice controls

Decision: decided by the user on 2026-11-25, from a review of the board page with 16 notes. The board changes as follows, and stays the same in every repository:

- the top bar holds the Frontdoor brand on the left, the page title centred, and the tools on the right; the rounds of the page move to a row of their own under it
- the brand is a drafting-table logo drawn straight on the bar, with no square or round shape around it, and the words `Frontdoor Design Board` in Fraunces 700, the face of the frontdoor banner
- the repository line above the page title, the round count, the round date and the recorded-choice pill are removed; the floating picked box already shows the choice
- the picked box, the round note and the Copy choice button float on their own, and the dock behind them has no background
- one variant per row, so a picture is shown large without opening the viewer
- Strengths, Risks and Known flaws become icons with a tooltip on hover
- more room between a picture's label bar and the picture

Why: three variants in one row made each picture too small to judge, so every picture needed the viewer; the header, the meta line and the recorded pill repeated what the board shows elsewhere [user].

Implementation notes: the font is a Fraunces subset of the letters in `Frontdoor Design Board`, about 2.8 KB, inlined as a data URL so the board names itself offline; optical size 18, because the optical size 144 the banner draws at 112 px made the 18 px words cramped on screen. Fraunces is under the SIL Open Font License 1.1, which allows embedding. In the one-per-row card the text sits in a 220 to 300 px column beside the pictures, and the picture height cap rises to the screen height less the header and the floating controls. The facts keep their words for screen readers in a visually hidden span [agent].

What breaks if ignored: a board that returns to three cards a row makes the user open every picture; a brand set in a fallback face reads as another product; the board's own look must not become the look of a repository it serves (FD-D38), so the brand stays the board's and never moves into a starter.

Rejected: loading Fraunces from Google Fonts - the board opens from `file://` and often offline, and the words would fall back to Georgia [agent].

Rejected: the banner's optical size 144 at 18 px - its thin strokes and tight spacing made the words hard to read [agent].

## FD-D44: defects found by the trial runs of the skills moved onto the core

Decision: lesson, recorded by the agent on 2026-11-24 during Phase 12.

Lesson 1, a false font WARN: in both trial runs `fd render` printed "fonts requested but not loaded" and exited 1 for Saira Extra Condensed, Libre Caslon Text and Old Standard TT, which were in the images. The check drew a hidden probe at weight 400 upright and compared its width with a fallback. A page that loads a family in weights 600 and 800 and uses only 800 never downloads the 600 face, and the probe at 400 matches that 600 face, so it measured the fallback while the font was on screen. It looked right because a family served in one face, or loaded from `local()`, passes: a first test built that way passed on the old code too. Fixed by counting a family as loaded when any of its faces in `document.fonts` has loaded, with the probe kept for system fonts; `tests/test_render_browser.py` serves one font file as weights 600 and 800 and fails on the old check [agent].

Lesson 2, gaps in the skill text that only a run showed: a variant folder seeded with `starter.html` had no `shared.css` or `shared.js`, so the page had no stylesheet and both themes rendered the same; `frontdoor-readme` building its own pictures was not told to copy `starter.css` as `shared.css`; the skills went to `fd round new` without `fd page add`; nothing said what an unattended run does at "show the board and wait"; nothing said how to show a design for a site with no dark theme. `board.md` and the three `SKILL.md` files now say each [agent].

What breaks if ignored: a render that exits 1 for a font that loaded teaches the agent to ignore the WARN, and then a font that really failed ships; a variant built from the seed alone shows one theme twice on the board.

Rejected: waiting for `document.fonts.ready` before the probe - the 600 face is never requested by the page, so nothing waits for it, and the probe itself would start the download only after it measured [agent].

Rejected: probing each family at the weight and style the page uses it at - it needs every weight and style collected per element, and `document.fonts` already says which faces loaded [agent].

## FD-D43: two defects found while building board v2

Decision: lesson, recorded by the agent on 2026-11-24 during Phase 11.

Lesson 1, `[hidden]` lost to the page's own display rules: the Pick button of the viewer, the Compare button and the dock were hidden with the `hidden` attribute, but `.btn { display: inline-flex }` and `.dock { display: flex }` override the browser's `[hidden] { display: none }`, so the Pick button still showed in the comparison view and the dock would have shown on a draft round. It looked safe because `hidden` works on an element with no display rule. Seen in the first comparison screenshot; fixed by `[hidden] { display: none !important; }` in the page [agent].

Lesson 2, a pipe from Windows PowerShell 5.1 corrupts the copied choice: `"..." | fd choose --from -` recorded the note `giữ thanh bên` with every Vietnamese letter as `?`, because PowerShell 5.1 encodes what it pipes to a native program in the console code page, before `fd` can decode UTF-8. A file written by the agent keeps the text, so `board.md` tells the agent to save the pasted text to a file and run `fd choose --from <file>`, and names the pipe as working elsewhere [agent].

What breaks if ignored: a control that must not be used in a view is shown and works there; a user's note in any language outside ASCII is stored as question marks in `board.json` with no error.

Rejected: decoding stdin in `fd` with another code page - the characters are already lost before `fd` reads them [agent].

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

## FD-D25: motion carries the landing page; under reduced motion ambient motion stops and clicks still animate

Decision: the hero of a landing page is an animated inline SVG figure of the product's own flow that the visitor drives (a start button, a clickable control inside the figure, a reset, an `aria-live` status line), each rough direction carries one, and the guidance lives in `frontdoor-landing/references/motion.md`. Under `prefers-reduced-motion: reduce` ambient motion (autoplay, loops, pulses, scroll reveals) is off and the first view is a meaningful state, while motion the visitor starts with a click still runs once at about a third of the duration; no control is hidden or becomes a no-op. `shoot.py check --click <selectors>` clicks each control with and without reduced motion and fails when the screen does not change. The `page-craft.md` sentence "with it, content is visible immediately and nothing moves" is replaced.

Why: Windows Settings > Accessibility > Animation effects off makes Edge and Chrome report `reduce` to every page, and many users switch it off for speed, so "nothing moves" removes the page's main content for a large share of Windows visitors.

Lesson, observed 2026-10-20 on the `commit-composer` landing page in Edge on Windows: five rough directions (rounds 5 and 6) were still sketches or reused the README images and did not convince the user; the user chose the one whose hero was a yard that runs on a click and said animation is the key. The first build followed the old rule: under reduce it hid Pause, drew only the end state, and Replay did nothing on the user's machine, which had animation effects off; `shoot.py check` passed it with 0 FAIL because nothing clicked anything. The fix made the run approve-driven (it waits at the plan for the visitor, as the product waits for approval) and let a click animate under reduce at 0.35 of the duration.

What breaks if ignored: dead buttons and a hero frozen at its end state for every visitor with reduced motion, and no check that reports it; a hero that autoplays past a human step claims the product skips it.

Verified 2026-10-21 with Edge: `shoot.py check` on the commit-composer page with `--click "#run,#reset"` printed ok for both controls in both modes, 0 FAIL; a copy whose `approve()` returns early under reduce printed `FAIL click #run (reduce motion): nothing on screen changed after the click`. Hovering and focusing before the first shot keeps a focus ring from passing a dead button, which an earlier version of the check did.

Not verified: a full `frontdoor-landing` run that follows the new text; Firefox and Safari; macOS "Reduce motion" (FD-Q3). Under normal motion an ambient loop on screen can mask a dead control, so the reduced run is the one that counts.

Rejected: stop all motion under reduce and hide the controls (the previous rule) - the page reads as broken and its buttons do nothing.

Rejected: ignore the setting - ambient loops and large movement are what it exists to stop.

Rejected: an autoplaying loop in the hero - it plays past the step where the product waits for a human, and nobody asked for it.

Rejected: animated rendered images (GIF, video) - heavy, not themable, and not interactive.

## FD-D26: a fourth skill, `frontdoor-ui-gallery`, moved to the ui-gallery pack

Moved to the `ui-gallery` pack as UG-D1 (the skill and its origin in `docker-zero`). This number stays reserved and is not reused.

## FD-D27: the gallery page's neutral look, moved to the ui-gallery pack

Moved to the `ui-gallery` pack as UG-D2. This number stays reserved and is not reused.

## FD-D28: where a gallery lives, moved to the ui-gallery pack

Moved to the `ui-gallery` pack as UG-D3. This number stays reserved and is not reused.

## FD-D29: the two pillars of stack references, moved to the ui-gallery pack

Moved to the `ui-gallery` pack as UG-D4. This number stays reserved and is not reused.

## FD-D30: how a state is mocked and shot, moved to the ui-gallery pack

Moved to the `ui-gallery` pack as UG-D5. This number stays reserved and is not reused.

## FD-D31: one design board per purpose

Decision: keep one board per purpose in its own folder, `.frontdoor/readme/`, `.frontdoor/landing-page/` and `.frontdoor/product/`, each with its own `directions.json`, `directions.html` and `round-<N>/`; `board.py` takes that folder as `<dir>`, derives the project name from the repository folder, adds `.frontdoor/` to `.gitignore`, and exits 1 for any other folder. `frontdoor-readme` uses `readme`, `frontdoor-landing` uses `landing-page`, and `frontdoor-illustrate` uses `product` for pictures of the product itself unless a caller hands it its own purpose. Amends FD-D24.

Why: one flat board mixed the directions for the README, the landing page and the product pictures, so rounds of unrelated work were compared and numbered together (an awsketch run kept hero rounds and product rounds apart by hand, in `branding/` and `product/`).

What breaks if ignored: round numbers and chosen directions of one purpose appear on the board of another, and the user picks from the wrong list.

Not verified: `product` is assumed to cover the product's own screens and scenes; `frontdoor-ui-gallery` does not use a board, so no skill writes to `.frontdoor/product/` except `frontdoor-illustrate` on request.

Rejected: a board per skill - `frontdoor-illustrate` is called by both other skills and would have no purpose of its own.

Rejected: keeping `.frontdoor/directions.html` and tagging rounds by purpose - the rounds stay in one list, which is the problem.

Rejected: free folder names - skills would invent different names and the guard in `board.py` could not catch a misplaced board.

## FD-D32: banner and banner-social, GitHub's social preview rules, an optional animated banner

Decision: name the README banner item `banner` (`banner.webp`, `banner-dark.webp`) and the GitHub social preview item `banner-social`; an `.item` marked `data-social` is 640x320 CSS px, rendered by `render.py` to `<id>.png` and `<id>-dark.png` at 1280x640 with no rounding and no border, with warnings for a size other than 1280x640, a file over 1 MB, text inside the 40 px safe border and more than one text block (headings, paragraphs, list items outside `data-bleed`), so a tagline under the name is caught. GitHub's rules, kept in `frontdoor-readme/references/banner.md`: set by hand in Settings, Social preview; at least 640x320 and 1280x640 for best display; PNG, GIF or JPG only; under 1 MB; a 40 pt border (80 px at 1280x640) free of important content. The social preview is always a still PNG, 1280x640 (at least 640x320), under 1 MB, with the 40 pt safe border; never a GIF and never a JPG. A moving README banner is optional: `frontdoor-readme` suggests it, briefs the user on the motion and its costs, asks first, and builds it only on approval with `frontdoor-readme/scripts/animate.py` (a slow sine sway, 90 frames at 10 per second, one palette, no rounding, `banner.gif` and `banner-dark.gif`). Extends FD-D18.

Why: the social preview was the one picture the skills did not produce, and a first attempt broke three GitHub rules at once; fixed names let the next run find the files.

Lesson: a banner turning a full circle at about 60 degrees per second made the reader dizzy, so the motion became a sway of about 20 degrees per second at its peak; a 1280x640 GIF came out near 2 MB and the upload refused it ("Please upload a picture smaller than 1 MB"); pasting the wide banner onto a plain 1280x640 ground cut its rings at the banner's top and bottom edge and put it against the right edge, outside the safe border, so the social card is composed on its own, with the wordmark inside the border and the decoration bleeding off the edge. A first answer shrank the social GIF to 672x336 with 64 colours (0.82 and 0.98 MB) to fit the limit; the user then found that messaging services show no thumbnail for a GIF link, so the social preview became a still image and the GIF applies to the README banner only. Measured on the awsketch social card at 1280x640: PNG 155 KB light and 167 KB dark, JPG 90 and 88 KB at quality 90 (75 and 74 KB at 85), so either format is far under 1 MB; JPG is lighter for gradients and many small icons, PNG keeps thin lines and small text crisp. The user chose PNG: a saving of about 65 KB on a picture fetched once and cached is not worth a lossy format. The first awsketch card also carried the tagline under the wordmark; the user pointed out it cannot be read in a messaging thumbnail, so the card now holds only the brand name (left) and the branding element (right), with the name larger.

What breaks if ignored: a social image in WebP or over 1 MB is refused by the upload; a GIF social preview shows no thumbnail when the link is pasted into a chat or mail app; a tagline on the card is unreadable at thumbnail size; a wordmark in the outer 80 px is cropped by the card; a fast or looping spin is a vestibular problem in a README that cannot honour a reduced-motion setting; a GIF made without asking adds 3 to 4 MB to every first view of the README.

Not verified: the social preview in a real share card (Slack, Teams, mail); the GIF banner on github.com in dark mode and on a phone; `animate.py` and `render.py` on macOS and Linux (FD-Q3).

Rejected: a GIF by default - it costs file size, colour depth and the rounded border, and the motion is a taste the user decides.

Rejected: a GIF social preview (even under 1 MB at 672x336) - GitHub accepts it, but chat and mail apps show no thumbnail for it, and which frame an unfurler takes is not under our control.

Rejected: a JPG social preview, or a JPG fallback when the PNG is over 1 MB - it saves about 65 KB on an illustrated card and is lossy around small text; an over-size PNG is fixed by simplifying the picture.

Rejected: a social preview in WebP with the rounded border - GitHub does not accept WebP, and a rounded image shows its corners as a plain rectangle.

Rejected: a continuous full-circle spin - it cannot loop with few frames when the shapes carry different icons, it needs over 150 frames, and it was too fast to read.

Rejected: rotating a group of shapes and icons - the icons turn with it, which the AWS trademark guidelines forbid; the drawing places each icon at its new coordinates instead.

## FD-D33: animated WebP is the only animated format; the banner shows under reduced motion

Decision: decided by the user on 2026-11-19. Every moving picture is an animated WebP made by `frontdoor-readme/scripts/animate.py` (`--motion sway` for a back-and-forth, `--motion loop` for a cycle, 30 frames at 12 per second, quality 68, rounded and bordered like the stills, under 700 KB per file); no GIF is built anywhere. The animated README banner keeps the names `banner.webp` and `banner-dark.webp`, and the README `<picture>` carries no `prefers-reduced-motion` source, so it moves for every reader. `frontdoor-illustrate` names the script as the way to animate. Amends the GIF part of FD-D32; the social preview stays a still PNG.

Why: the same 30 frames of a 1200x420 banner were 3.0 MB as GIF and 306 KB as WebP (7.6 MB against 650 KB at 2400x840), and WebP keeps 24-bit colour and the rounded border that a GIF loses [user]. The user wants the banner visible on every machine, including those with reduced motion enabled [user].

What breaks if ignored: a GIF adds several MB to every first view of the README and loses the rounded border; a reduced-motion source in the `<picture>` shows those readers the still, which the user does not want; a second animation tool for GIF drifts from the WebP one.

Not verified: the animated WebP on github.com in light and dark and on a phone; macOS and Linux (FD-Q3); mail clients and apps that do not play animated WebP. A reader who enabled reduced motion now sees movement by design, which is why the motion stays slow and small.

Rejected: keeping GIF as an option beside WebP - the user chose one format, and the GIF is about ten times larger [user].

Rejected: a `prefers-reduced-motion` source that serves the still banner - the user wants the banner to show on every machine [user].

## FD-D34: `animate.py` encodes at libwebp effort 4 in worker processes, and animations run one at a time

Decision: decided by the user on 2026-11-24. `frontdoor-readme/scripts/animate.py` takes `--method` (default 4) instead of the fixed `method=6`, writes each finished frame to a temporary PNG and encodes each theme in a worker process (two at most) while the next theme is captured, and prints the seconds each encode took; `banner.md` tells the agent to run one animation at a time and gives the settings that kept a ripple banner under 700 KB (about 1500 px wide, `--frames 20`, `--quality 55`).

Why: with `method=6` one 2400x840, 30-frame banner took about 11 minutes to encode and came out at 1.0 MB, over the 700 KB limit of FD-D33, while capturing the frames took well under a minute [agent]. With the new defaults, one banner and three diagrams at 1500 px wide and 20 frames took 7 to 22 seconds per file, 411 to 604 KB, 4 minutes for all four pictures in both themes [agent]. The user chose to fix the script before rendering the rest [user].

What breaks if ignored: an agent follows the documented defaults on a line-heavy banner, waits many minutes per file, and still gets a file over the limit. Four animations run at once exhausted the memory of the machine; the system stopped them and left the light-theme files and one dark file at 0 bytes, which broke the README until the stills were rendered again.

Not verified: how much of the speed-up comes from `--method 4` and how much from the smaller size, fewer frames and lower quality, because no run changed only the method; the file-size cost of `--method 4` against 6 on the same frames; macOS and Linux (FD-Q3), where worker processes start by fork and not by spawn.

Rejected: keeping the script and only lowering `--size`, `--frames` and `--quality` for the banner - the user ruled for the script fix first [user].

Rejected: rendering several animations in parallel - memory ran out and the runs were stopped [agent].

Rejected: dropping the animations and keeping the stills - the user asked for the animation [user].

## FD-D35: `animate.py` encodes each frame in its own worker and joins the animated WebP itself

Decision: decided by the user on 2026-11-24 ("apply every option, as long as it speeds up the render"): `frontdoor-readme/scripts/animate.py` encodes every frame as a still WebP in a pool of `--workers` processes and writes the animated WebP container itself, captures the themes in parallel, captures a repeated sway value once, and offers `--draft` and `--batch`; the pipeline is in `sourcecode` under `Scripts`.

Why: Pillow's animated save runs libwebp's `WebPAnimEncoder` on one core per file. On this machine (8 CPUs) the Skillmesh loop banner (2400x880, 40 frames) went from 111 s at 706 / 728 KB to 22 s at 311 / 324 KB, and the Homeware sway banner (2400x800, 30 frames, 15 drawn) from 46 s at 321 / 255 KB to 18 s at 188 / 143 KB, at the same PSNR against freshly captured frames (old / new: 37.3 / 37.2 dB and 37.8 / 37.8 dB mean) [agent]. Before the change, per frame, the border finish cost 0.6 s (two 32 MP masks), a still frame at method 4 0.8 s and an animated frame about 1.5 s on one core [agent]. The two banners in one `--batch` run took 25 s against 40 s as two runs; a draft took 12 s [agent].

What breaks if ignored: going back to `WebPAnimEncoder` puts the encode on one core per file again, and a long or line-heavy banner takes minutes per run.

Not verified: macOS and Linux (FD-Q3), where workers start by fork; a page whose drawing changes nearly every pixel each frame, where the rectangle and block savings are small and the file may grow against `WebPAnimEncoder`; memory on a machine with many CPUs and little RAM, where `--workers` must be lowered by hand; the files on github.com.

Rejected: libwebp's own `thread_level` - Pillow does not expose it [agent].

Rejected: ffmpeg, `img2webp` or `webpmux` - a binary outside the skill folder, against the rule that a skill runs alone [agent].

Rejected: `--method 0` as the fast setting - on one 2400x840 frame it took 2.2 s against 0.8 s for method 4, for a file half as large again [agent].

Rejected: the 3 px border and 24 px radius applied unscaled at the output size - at 1500 px wide the corners and border would read thicker than the still pictures at the same display width [agent].

## FD-D36: a `frontdoor-core` skill holds the shared core, and the other skills require it

Decision: decided by the user on 2026-11-24. Add a skill `frontdoor-core` that holds what the skills share: the signature method (`signature.md`), the design board method and its harness `fd` (FD-D37 to FD-D41), the render contract widened to any item size (icons, components, banners), and `animate.py`. `frontdoor-readme`, `frontdoor-illustrate` and `frontdoor-landing` keep only what is theirs (the banner and social preview stay in `frontdoor-readme`), find the core at `<skill-dir>/../frontdoor-core`, and stop with a message to install `frontdoor-core` when it is missing. The core can be invoked on its own, so a user can make an agent follow the frontdoor principles in work no frontdoor skill covers, such as redesigning one component of a web page. Reverses FD-D2 (each skill self-contained) and FD-D22 (three byte-identical copies of `signature.md`), and the three copies of `board.py` in FD-D24. Not implemented yet: Phase 10.

Why: the workflow is tied to the README use case, so other work has no skill and the user has to say "apply the design board philosophy of the frontdoor skills" by hand [user]. One copy of the core replaces three copies kept equal with `cmp` [agent].

What breaks if ignored: a skill installed alone stops at its first step; the `AGENTS.md` rule "A skill must run alone" and the `cmp` rule for `signature.md` and `board.py` contradict the code until they are rewritten in the same change.

Rejected: a copy of the core inside each skill, synced by a repository script and compared with `cmp` (the agent's recommendation) - the user chose a required core [user].

Rejected: the harness published as a package that the skills run through `uvx --from git+...` - it needs the network on every run and a pinned version [agent].

Rejected: a core that is only a library and cannot be invoked - the user wants it callable for use cases outside the repository's skills [user].

## FD-D37: one board per repository, a page per use case, rounds numbered per page

Decision: decided by the user on 2026-11-24. Keep one design board per repository, under `.frontdoor/board/`, ignored by git. A page is one use case with a free slug (`readme`, `icons`, `navbar`), created by `fd page add <slug>`; the rounds of a page are its panes, shown as tabs, and each page numbers its own rounds from 1. Boards made before this change (`.frontdoor/readme/`, `.frontdoor/landing-page/`, `.frontdoor/product/`) are not migrated: a user who takes the new skills decides what to do with them. Reverses FD-D31 (one board folder per fixed purpose) and the board location of FD-D24. Not implemented yet: Phase 11.

Why: rounds of unrelated work share one numbering; icons put on the board during README work became rounds 4, 5 and 6 instead of 1, 2 and 3, because icons had no purpose of their own [user]. A fixed list of purposes cannot hold use cases outside the README, the landing page and the product [user].

What breaks if ignored: a new kind of work lands on the board of another purpose and continues its round numbers, and the user picks from the wrong list.

Rejected: the fixed purpose list of FD-D31 - it is the cause of the problem above [user].

Rejected: a page per use case with a pane per sub-subject (banner, scenes) and the rounds inside each pane - the user chose rounds as the panes [user].

Rejected: a board folder per purpose, as now - the user wants one board split into pages and panes [user].

Rejected: an `fd board migrate` command for old boards - the user leaves old boards to the user who takes the new skills [user].

## FD-D38: the board is a neutral harness page with a hover table of contents, one frame per image and a theme divider

Decision: decided by the user on 2026-11-24. The board ships one neutral look, the same in every repository, because it is part of the harness and not a product of frontdoor; the `AGENTS.md` rule against shipping a reusable look applies to what the skills make for a repository, not to frontdoor's own tooling. Its interface:

- a floating table of contents on the left, collapsed by default to a narrow rail, expanding on hover and covering the content instead of pushing it; the tree is page, round, variant, with the chosen variants marked
- one frame per image holding both themes, with a light/dark switch, and an interactive mode in which hovering the image draws a divider that shows the two themes on its two sides; light against dark is the default comparison
- a comparison of two variants against each other is available but off by default; the agent asks the user whether to turn it on for a round
- long images fit the screen inside their card and open in a viewer that zooms and scrolls

The board's interface is designed with the `impeccable` and `design-taste-frontend` skills; they are used to design the board itself and are not part of the frontdoor workflow. Not implemented yet: Phase 11.

Why: the current board is one 1080 px column in which each image takes the full width and the light and dark images stack; on the `docker-zero` product board (one round, three variants, images of 1040x1920, 1040x1620 and 1040x1626 px) one round is a scroll of about 11,000 px [agent]. The user finds the board hard to use with long images and hard to move through when there are many variants and rounds [user].

What breaks if ignored: a board styled with a repository's signature biases the comparison toward the direction that looks like it, and has no signature to use in the first round, which is the round that chooses one [agent].

Rejected: the board in each repository's signature - the board is a harness and must look the same wherever it is used [user].

Rejected: the light and the dark image as two stacked pictures - it doubles the length of every round [user].

Rejected: the two-variant comparison as the default view - the user wants it offered, not assumed [user].

Rejected: `impeccable` and `design-taste-frontend` as steps of the frontdoor skills - they are for designing the board's interface only [user].

## FD-D39: the choice returns through a copy button now, a local board server later

Decision: decided by the user on 2026-11-24. The board gets a "Copy choice" button that copies the chosen and mixed variants, with the user's notes, as text the user pastes into the chat (Phase 11). A local server, `fd board serve` on `127.0.0.1`, that records clicks into the board file for the agent to read is a later phase of its own (Phase 13). The board data is laid out in Phase 11 so the server can be added without changing it.

Why: the user chose the copy button first [user]. The server removes the copy and paste and mistyped variant ids, allows a note on each variant, reloads the board when a round is added and returns the choice as JSON, at the cost of a process that must be running, a token in the URL so another page cannot write to the board, a way for the agent to learn that a choice was made, and more code and tests [agent].

What breaks if ignored: a board data layout that has no place for choices and notes makes the server a rewrite.

Rejected: the choice told to the agent in free text, as now - variant ids are mistyped and the mix is lost [agent].

Rejected: the local server in Phase 11 - the user wants it as a separate phase [user].

## FD-D40: the number of variants is asked every round

Decision: decided by the user on 2026-11-24. Every round starts with a question to the user on how many variants to make, with a recommended number; `fd round new` takes `--count` as a required argument and has no default. With no user to answer, make 3 variants and write the question with that answer to `questions.md` (FD-D9). The wording "two or three" leaves the three `SKILL.md` files and `signature.md`. Not implemented yet: Phases 10 and 12.

Why: every round now makes two or three variants without asking, which is not the user's choice [user].

What breaks if ignored: an agent makes three variants when the user wanted one refinement, or two when the user wanted a wide search, and the work of the round is spent on the wrong number.

Rejected: a fixed "two or three" in the skill text - the user wants to be asked [user].

Rejected: 2 variants for an unattended run (the agent's recommendation) - the user chose 3 [user].

## FD-D41: the harness is Python run through uv, with a daemon that keeps the browser open

Decision: decided by the user on 2026-11-24. Write the harness `fd` in Python, run through `uv` / `uvx ... python -I` with Playwright and Pillow as now, and add a daemon that keeps one browser open between commands and serves render jobs on localhost, with a `--watch` mode that renders again when a source page is saved. Not implemented yet: Phase 10.

Why: measured on this machine (Windows, Edge, 8 CPUs) on 2026-11-24: starting `uvx python` took 0.20 s, the uvx environment with Playwright and Pillow 0.39 s, importing Playwright 1.03 s, launching Edge 0.52 s and opening a page 0.60 s, while encoding one 2400x960 lossless WebP took 3.39 s at `method=6` (what `render.py` uses) and 1.54 s at `method=4` for the same 74 KB file; `render.py` on one item in one theme took 7.9 s. The time is in libwebp and the browser, not in the language, so a rewrite in another language saves about the 1 s of the import, which the daemon removes as well [agent]. The user chose to keep Python and uv with a daemon [user].

What breaks if ignored: every repeated render pays for a browser start and a slow encode, and a rewrite in another language costs the working scripts without removing either.

Not verified: the daemon from a host whose shell ends detached processes; macOS and Linux (FD-Q3).

Observed 2026-11-24 on the 20 pictures of `assets/source/readme.html` and `scenes.html`: method 4 wrote 1837 KB against 1839 KB at method 6, the largest single file 1.7 percent larger, and every file pixel-identical to the `render.py` output, so 4 became the default [agent]. With capture and encode overlapped in a process pool the two pages took 12.5 s and 14.8 s against 40.7 s and 48.3 s for `render.py`; with the daemon running one item took 3.6 s against 5.7 s [agent].

Rejected: TypeScript on Bun or Node - Playwright is native there and the start is 0.08 s, but it needs `node_modules` installed or fetched per run and `sharp` for WebP, and every script is rewritten [agent].

Rejected: one Rust or Go binary - no Playwright, so the browser protocol is written by hand, and each skill would carry one binary per operating system, for about 1 s saved [agent].

## FD-D42: skills that help write the harness are installed at project scope and ignored by git

Decision: decided by the user on 2026-11-24. Install `astral-sh/agent-plugins@uv`, `astral-sh/agent-plugins@ruff`, `wshobson/agents@python-testing-patterns` and `steipete/agent-scripts@create-cli` at project scope in this repository, for the people and agents writing the harness, and add the installed skill folders and `skills-lock.json` to `.gitignore`. They are not frontdoor skills and do not ship.

Why: a survey of the skills ecosystem on 2026-11-24 (29 searches, the shortlisted `SKILL.md` files read in full) found these four as the closest fit for a Python CLI run through uv with a first pytest suite; nothing worthwhile was found for a daemon, IPC, a file watcher, or animated WebP [agent]. The user approved them and chose project scope and git-ignored folders [user].

What breaks if ignored: installed skill folders appear untracked beside the repository's own skill folders and can be committed as if they shipped.

Rejected: `trailofbits/skills@modern-python` - it covers the uv and ruff skills and adds a heavy setup (a Makefile, `select = ["ALL"]`, a coverage floor) [agent].

Rejected: the popular Playwright skills - their examples are TypeScript only, and the one Python skill tells the agent to run `playwright install`, a download of about 200 MB [agent].

Rejected: `jeffallan/claude-skills@cli-developer` - its Python reference pushes Typer, Click and Rich, against a small dependency footprint [agent].

Rejected: user scope - the user chose project scope [user].

## Open questions

### FD-Q1: do the skill descriptions make a host pick the skills on a plain request?

Selection was tested only by giving a subagent the skill path. The descriptions were written to be assertive and the optimizer in the skill-creator plugin was not run. What is at stake: a skill that is never selected is dead weight. Trigger to reopen: a plain request ("make the README nicer", "add a GitHub Pages site") that does not invoke the skill.

### FD-Q2: do the skills need automated tests?

Nothing checks the scripts or the skill text beyond `quick_validate` and the manual runs recorded in the roadmap. What is at stake: a later edit to `render.py`, `shoot.py` or `lighthouse.py` can break a path nobody re-runs. Trigger to reopen: the first regression, or a decision on where the skills finally live.

### FD-Q3: do the scripts work on macOS and Linux?

All runs were on Windows with Edge. `lighthouse.py` carries browser paths for macOS and Linux that were never executed, and `render.py` and `shoot.py` rely on Playwright's Edge and Chrome channels. What is at stake: a copy of the skills on another operating system fails at the first script. Trigger to reopen: a run on either system.
