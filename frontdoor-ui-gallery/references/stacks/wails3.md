# Wails v3

## Recognise it

`go.mod` requires `github.com/wailsapp/wails/v3`, and the frontend's `package.json` depends on `@wailsio/runtime` at the same version. Windows are created in Go with `app.Window.NewWithOptions(application.WebviewWindowOptions{...})`; their `Width`, `Height`, `Frameless` and `URL` give the view sizes and how a window selects its view (often a `?view=` query read by the root component).

## The seam

- **Generated bindings**: `wails3 generate bindings` writes one module per bound Go service under `frontend/bindings/<module path>/<package>/<service>.ts` (with `-ts`), plus `models.ts` per package. Each function calls `$Call.ByID(<id>, ...args)` from the runtime. The folder is usually gitignored; generate it when it is missing (`wails3 task` names the task, often `generate:bindings` or `bindings`; the plain command is `wails3 generate bindings -ts`).
- **A wrapper**: some apps re-export the bindings from one file (for example `src/wails.ts`). Mock the wrapper when it exists: it is the one module every component imports.
- **Events**: `Events.On("<name>", cb)` from `@wailsio/runtime`. The Go side registers each event type and emits it. A mock does not need to emit events when the state is complete in what the first calls return; push an event only for a state that exists only after one.
- **Runtime calls**: `Window.Hide()`, `Window.SetSize`, dialogs, clipboard. They are part of the runtime package, not the bindings; leave them alone unless a shot clicks one, and then stub that one function in the wrapper mock.

Replace the service modules (or the wrapper) only. Keep `models.ts` real: the mocks and scenarios import its types and enums, which is what makes a changed Go type fail the type check.

## Mock it

In `vite.gallery.config.ts`, match the service modules by the path end, for example

```ts
[/\/internal\/ui\/(service|settingsservice)(\.js)?$/, (m) => `${m[1]}.ts`]
```

or the wrapper by its specifier. Each mock file exports every function of the real module:

```ts
import type * as Real from "../../bindings/github.com/<owner>/<app>/internal/ui/service";
import { baseStatus, call, scenario, type Mocked } from "../fixtures";

const mock = {
  Status: () => call("Service.Status", { ...baseStatus, ...scenario.status }),
  Start: () => call("Service.Start", undefined),
} satisfies Mocked<typeof Real>;

export const { Status, Start } = mock;
```

`baseStatus`, `scenario` and `call` come from the scenario file made from `assets/fixtures.ts`. Wails rejects a failed call with an `Error` whose message is the Go error text, which is the `caller` default.

The binding functions return the runtime's `CancellablePromise`; `Mocked` maps them to a plain `Promise`, which every caller can await.

## In a plain browser

The runtime prints a "Browser Environment Detected" warning and keeps working; `Events.On` registers a listener that never fires. Without the mocks every binding call rejects, and the UI shows its error or loading state. Drag regions (`--wails-draggable`) and frameless window chrome render as plain elements.

## Versions

The generated file layout and the runtime API changed during the v3 betas. Read the generated files of the version the app pins before writing a mock, and keep the CLI, the Go module and `@wailsio/runtime` on that one version: the skill must not upgrade any of them.

| Version | Observed |
|---|---|
| `v3.0.0-beta.30` | six service modules under `frontend/bindings/<module>/internal/ui/`, `models.ts` interfaces and enums; mocked per service module |
| `v3.0.0-beta.8` | one service module under `frontend/bindings/<module>/internal/<package>/service.ts`; `models.ts` classes with `createFrom` and enums with a `$zero` member (object literals satisfy the classes, so `Mocked` works unchanged); a 404 console message in the browser, not a page error; mocked through the app's wrapper `src/wails.ts` |

Generate missing bindings with the CLI version the app pins, without installing it: `go run github.com/wailsapp/wails/v3/cmd/wails3@<pinned version> generate bindings -ts` from the repository root, with the flags of the app's own Taskfile task.
