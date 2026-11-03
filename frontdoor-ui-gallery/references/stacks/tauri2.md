# Tauri v2

## Recognise it

`src-tauri/tauri.conf.json` with `"$schema": "https://schema.tauri.app/config/2"`, and `@tauri-apps/api` 2.x in `package.json`. The `app.windows` array gives each window's `label`, `url` (often a separate HTML entry such as `break.html`), `width`, `height`, `decorations` and `transparent`. A window that Rust resizes at run time (`set_size`, a full-screen overlay) needs a per-state `size` in `gallery.json`.

## The seam

- **Commands**: `invoke("<command>", args)` from `@tauri-apps/api/core`. Rust lists them in `tauri::generate_handler![...]`. Apps often wrap every call in one module (for example `src/lib/ipc.ts`) with typed functions; mock that wrapper when it exists.
- **Events**: `listen("<event>", cb)` from `@tauri-apps/api/event`, often imported directly by a composable or store, not through the wrapper. Mock that module too, and call each listener once with the scenario's payload so the view shows the state.
- **Plugins**: `@tauri-apps/plugin-*` packages (store, dialog, fs, shell). Mock each one the frontend imports; leave alone the ones only Rust uses.
- **Types**: there are no generated bindings unless the app uses `tauri-specta` or `ts-rs`. The frontend's own types file (for example `src/lib/types.ts`) mirrors the Rust structs; type the scenarios with it. Command names are plain strings, so check the mocked list against `generate_handler!` by reading it, and say in the report that the check was by reading.

## Mock it

Prefer replacing the wrapper and the event module by path:

```ts
[/\/lib\/ipc(\.ts)?$/, () => "ipc.ts"],
[/^@tauri-apps\/api\/event$/, () => "event.ts"],
```

`satisfies Mocked<typeof Real>` against the wrapper keeps its functions in step. The event module exports far more than the app uses, so type its mock with the functions the app imports: `satisfies Mocked<Pick<typeof Real, "listen">>`; a newly imported event function then fails only at run time, so say so in the report. A mock for `listen` returns an unlisten function and calls the callback with `{ event, id: 0, payload }` after a short delay.

A failed `invoke` rejects with the value Rust returned, a bare string for `Result<_, String>`, not an `Error`: set `rejectWith: "string"` on the scenario file's behaviour.

The regular expression is matched against the specifier as written, so `[/\/lib\/ipc(\.ts)?$/, ...]` also catches an alias import such as `@/lib/ipc`.

When the app has no wrapper and calls `invoke` everywhere, replace `@tauri-apps/api/core` with a module whose `invoke(cmd, args)` looks the command up in the scenario. `@tauri-apps/api/mocks` (`mockIPC`) is an alternative that needs no alias; check that the installed version mocks the events the app listens to before relying on it.

## In a plain browser

Without the mocks `invoke` rejects because `window.__TAURI_INTERNALS__` is missing, so the UI shows its loading or error state; `listen` rejects too and may leave an unhandled rejection. Each HTML entry is its own page on the Vite server (`/break.html?state=...`). A `transparent` window draws on nothing: set `omitBackground` for the view so the shot keeps its alpha, and say so in the view's `opens`.

The Vite config often sits at the repository root while the frontend source is in a folder such as `src-vue/`: put the `gallery/` folder in the source folder, so the existing type-check include covers it, and point the gallery config's `mockDir` there.

## Rules these apps tend to carry

Rust owns the timers and the business state: a mock delivers what Rust would send (a snapshot, a tick), it never moves logic into the browser. Do not add dependencies or change Rust code for the gallery.
