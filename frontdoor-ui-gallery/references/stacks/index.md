# Stacks

Every app has two pillars: the backend the frontend talks to, and the framework the frontend is written in. Read one file of each. The backend file says where the seam is and how to mock it; the frontend file says how to find the states in the templates and how to type-check the mocks.

| Backend | File | Frontend | File |
|---|---|---|---|
| Wails v3 (Go) | `wails3.md` | Svelte 5 | `svelte.md` |
| Tauri v2 (Rust) | `tauri2.md` | Vue 3 | `vue.md` |

Combinations run with this skill so far:

| Combination | Status |
|---|---|
| Wails v3 `beta.30` + Svelte 5 + Vite 8 | run end to end: 5 views, 50 states, real references |
| Wails v3 `beta.8` + Vue 3 + Vite 6 | run end to end by a fresh agent: 2 views, 29 states, mocked through the app's wrapper; no real references |
| Tauri v2 + Vue 3 + Vite 8, two HTML entries | run end to end by a fresh agent: 3 views, 19 states, wrapper and event module mocked, transparent break window; no real references |

Every frontend here is served by Vite, so the mock harness is one Vite config (`assets/vite.gallery.ts`) that resolves the seam modules to mocks. For a backend or framework with no file here (Electron, React, a plain web app calling `fetch`), apply the same rules and say in the report that the stack is not covered: find the narrowest module the UI calls the backend through, replace it with typed mocks in a separate dev config, and find the states in the template's conditionals.

## Adding a stack

A new file covers one pillar only, with the same sections as its siblings: how to recognise it, where the seam is, how to mock it, what breaks in a plain browser, and the commands. Add its row to the first table and its combination, once run, to the second.
