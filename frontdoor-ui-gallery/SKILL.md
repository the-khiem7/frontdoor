---
name: frontdoor-ui-gallery
description: Catalogue every screen and state of a desktop or web app's UI (loading, empty, busy, every error, confirmations, first run) by rendering the real frontend in a browser with its backend calls mocked, and publish one gallery page with light and dark screenshots, observed UI defects, screenshots of the built app, and a Keep / Revise / Discuss review per state. Use whenever the user wants an overview, inventory, audit or screenshot set of an app's current UI, wants to plan or review a UI redesign, wants before and after screenshots of a UI change, or needs real app screenshots for a README, for Wails, Tauri or Vite frontends in Svelte or Vue, even if they never say "gallery".
---

# UI gallery

A redesign starts from what the app shows today, in every state, not only the happy path a screenshot by hand catches. The gallery renders the real frontend in a browser with the backend replaced by fixed data per state, so every state is on screen on demand, in light and dark, and can be re-shot after each change. It is a working tool for the people building the app, so its page has one neutral look and no repository signature.

## Workflow

1. **Read the repository.** Read `AGENTS.md`, `CONTRIBUTING.md` and any rules that bind code or committed files: a ban on comments, on new dependencies, on committing generated files, a public-repository rule against user names and paths. Find which linters and formatters cover the folders you will add (`biome.json`, ESLint, Prettier, CI steps): format what you add with the repository's own formatter, and when a linter would fail on `design/ui-gallery/`, say so in the report and leave its config alone unless the user agrees. Identify the backend and the frontend framework, then read `references/stacks/index.md` and the two files it points to, one for each. When the UI is not a web frontend, say so and offer screenshots of the built app only (`references/real-capture.md`).
2. **Find the seam and make the frontend start.** Find where the frontend calls the backend, and pick the narrowest module to replace: the app's own wrapper when it has one, else the generated bindings, else the platform package. Install the frontend's dependencies with its own package manager; when that manager is not installed, ask, or in an automated run use npm with `--no-package-lock`, and never change a lock file. Generate missing bindings with the tool version the app pins, never a newer one. Both steps are local and change no committed file.
3. **List the states before writing a mock.** Follow `references/states.md`: every view, and for each the states its code can reach, with the data that drives each one taken from the backend's real types, enums and error texts. Write the list into `gallery.json` first; it is the contract for the mocks. A state you leave out on purpose goes under `skipped` with the reason.
4. **Build the mock harness.** In a `gallery/` folder inside the frontend's source, copy `assets/mock-kit.ts` and `assets/fixtures.ts`, then write one mock per replaced module, each typed against the real module as `mock-kit.ts` shows, so a changed backend fails the type check instead of the gallery. Serve it with a separate dev config made from `assets/vite.gallery.ts` and a `gallery` script; add the `gallery/` folder, not the config, to the type check. The production build must not import any of it. Strip the comments from every file you copy (the page and the config included) when the repository forbids comments.
5. **Render.** Put `gallery.json` (`references/manifest.md`) in `design/ui-gallery/`, which is committed so a later change can be compared with it, and copy `assets/gallery.html` there as `index.html`. Start the gallery dev server on the port `base` names, then run

   ```
   uvx --from playwright --with pillow python -I <skill-dir>/scripts/shoot.py render design/ui-gallery/gallery.json
   ```

   It writes `shots/<id>-<theme>.webp` and `gallery-data.js`; `--only a,b` re-shoots some states and still refreshes every text from `gallery.json`. It stops on a page error, a click whose target is missing or ambiguous, or a crop that finds less than it names.
6. **Look at every image** in both themes. When something looks wrong (text cut off, an error that never shows, a control enabled when it can only fail, contradictory messages), confirm it in the DOM or the code before writing it into the state's `note`; a note says what the screen shows, never that the real app behaves so at run time.
7. **Shoot the built app** when it runs on this machine: the main views, with `scripts/real.ps1` on Windows (`references/real-capture.md`), account paths painted over, listed under `real` in `gallery.json` and rendered again so the page pairs them with their mock. Restore any setting you toggled to reach a window.
8. **Verify.** Run the frontend's type check and production build, and confirm the built bundle holds no fixture text. Run `shoot.py check design/ui-gallery`, which fails on page errors, missing or broken images and horizontal overflow at 390 and 1440 px, and look at its screenshots. Search the added files for the user's name, machine name and home path, and look at the images for them: text inside an image cannot be searched.
9. **Report and stop.** List the files added, the state count per view, the observations, the size of `shots/`, how to regenerate (the dev server command with its port, then the render command), and what was not checked (the mocks against the live backend, other browsers, lint rules you could not run). Leave everything uncommitted.

## When no user can answer

Take the recommended default, write each question with the answer you assumed to `design/ui-gallery/questions.md`, and continue. Do not stop to ask in an automated run.

## Pitfalls that cost time before

- A dev server started in the background keeps running after its shell task is stopped, and holds the frontend folder open; end its node process (match the command line and the repository path) when you are done.
- The app's own timers move a state on: a poll that clears an error, a timeout that hides a notice. Set `"timers": "paused"` on the view (`references/manifest.md`) so every wait advances the clock by exactly its length, instead of racing them with short waits.
- A success notice next to controls that still show the old value is a state the app never shows. Keep what a command changes in the scenario file's `store`, so the reload after a save returns what was saved.
- Two controls with the same name (a radio label in two groups, several "minutes" fields) make a click ambiguous: scope it with `within` or pick one with `nth`; a control with no name is reached with `selector`.
- An error line inside a fixed-height window can be squeezed to zero height and never show; measure the element when a shot shows no error where one is expected.
- On Windows, Git Bash `sed -i` drops CRLF line endings and Python `Path.write_text` writes them: keep each edited file's existing endings.
- Python on Windows prints with the console code page; the script reconfigures stdout, so do the same in any helper that prints page text.
