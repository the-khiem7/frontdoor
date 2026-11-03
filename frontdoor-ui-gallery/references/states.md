# Listing the states

A gallery is only as useful as its list. A state missing from it is a screen the redesign never sees; a state invented for it is a screen nobody will ever meet.

## Where the states come from

Read each view's template and the code that feeds it, not the README. A state is a distinct thing the user can see, reached by data, by a click, or by time:

- **Data**: every branch of the template (`{#if}`, `v-if`, `v-show`, ternaries, class bindings) and the field values that select it. Follow each field back to the backend type that fills it and take its real values: enum members, status strings the backend prints, the exact error texts it returns (`errors.New`, `fmt.Errorf`, `Err(...)`, thrown messages). Never write an error text the backend cannot produce.
- **Clicks**: local UI state the data does not show: a confirmation panel, an open form, a validation message, a second step. Reach it with `actions` in `gallery.json`, not with a fake scenario field.
- **Time**: the moment before the first data arrives (loading), a call in flight (busy, spinner, disabled controls), the result after it (success notice, error). Hold a busy state with a call that never settles (`hang`).

## The checklist per view

Go through it for every view. A state that cannot occur or cannot be shown goes under `skipped` in `gallery.json` with the reason, so the list is complete on purpose and the page says what was left out:

| State | What to look for |
|---|---|
| Loading | the first frame before any call returns |
| First run | nothing installed, configured or signed in yet |
| Typical | the state most users see most of the time |
| Empty | lists with no items, values not set |
| Busy | each long action while it runs |
| Success | each notice or result after an action |
| Each error | every error path the view can show, with the backend's text |
| Confirmation | every are-you-sure step |
| Validation | every form message the frontend writes itself |
| Long content | the longest realistic text: paths, names, logs, many items |
| Limits | content taller than the window: shoot the full height, the page marks where the window ends |
| Platform gaps | the backend feature missing (no WSL, no permission, offline) |

## Data in the scenarios

- Use placeholders for anything personal: a user named `you`, `C:\Users\you\...`, `example.com`, a made-up certificate thumbprint. The gallery is committed and may be public.
- Keep values deterministic: fixed timestamps, fixed versions, no `Date.now()` or random ids in what is drawn. Set the view's `clock` when the UI prints the time or a greeting.
- A scenario is named for what the user sees (`stopped`, `update-failed`), and one scenario may serve several views.
- A call the frontend repeats (a poll, a refresh after each action) returns the same data every time, unless a command changed it. A command changes the scenario file's `store` (a saved setting, a paused flag), and the next read returns the store, so a success notice appears beside controls that agree with it. The store starts from the scenario on every page load, so each shot is the same in every run.
- Reject the way the backend does: an `Error` with the text for Wails and HTTP clients, the bare string for a Tauri command that returns `Result<_, String>` (`rejectWith` in `mock-kit.ts`). The UI often prints `String(err)`, and an `Error:` prefix in a shot is a state the app never shows.
- A state that lasts only until the app's own timer fires (an error the next poll clears) is shot with the view's `timers` paused, not by racing the timer.

## Observations

While looking at the images, note what a redesign must fix: text cut or squeezed out of view, an error that never shows, a control enabled when it can only fail, two messages that contradict each other, a busy state that leaves the user nothing to watch, a state with no way forward. Confirm each in the DOM (measure the element, read its computed style) or in the code before writing it, and write what the screen shows in one sentence. A note never claims how the built app behaves at run time; the mocks only prove what the frontend draws for the data they return.
