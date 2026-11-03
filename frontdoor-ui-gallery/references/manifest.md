# gallery.json

One file in `design/ui-gallery/` describes the gallery: the views, the states, the states left out and the real references. `shoot.py render` reads it; the gallery page reads what render writes from it (`gallery-data.js`). Write it as JSON with two-space indentation, every array expanded, and LF line endings, so a tool and a person produce the same diff.

```json
{
  "title": "Example UI gallery",
  "lede": "Every window and state of the app as it looks today ...",
  "base": "http://127.0.0.1:9246",
  "regenerate": [
    "cd frontend && GALLERY_PORT=9246 npm run gallery",
    "uvx --from playwright --with pillow python -I <frontdoor-ui-gallery>/scripts/shoot.py render design/ui-gallery/gallery.json"
  ],
  "storageKey": "example-ui-gallery",
  "scale": 2,
  "quality": 80,
  "defaults": {
    "scroller": "main"
  },
  "views": {
    "settings": {
      "title": "Settings",
      "short": "Settings",
      "size": [
        520,
        680
      ],
      "source": "frontend/src/Settings.svelte",
      "opens": "Gear in the popup, or Settings... in the tray menu.",
      "url": "/?view=settings"
    }
  },
  "states": [
    {
      "id": "settings-busy",
      "view": "settings",
      "state": "settings-busy",
      "title": "Working",
      "how": "A setting is being applied.",
      "note": "Working... appears below the fold of the 680 px window.",
      "actions": [
        {
          "click": "Desktop",
          "role": "checkbox"
        }
      ],
      "crop": "full"
    }
  ],
  "skipped": [
    {
      "view": "settings",
      "state": "Applying",
      "why": "Set and cleared under one lock in the backend; the frontend can never read it."
    }
  ],
  "real": [
    {
      "id": "real-settings",
      "view": "settings",
      "pair": "settings",
      "title": "Settings, built app"
    }
  ]
}
```

## Top level

| Key | Meaning |
|---|---|
| `title`, `lede` | heading and one-line description of the page |
| `base` | where the gallery dev server listens; `--base` overrides it. Pick a free port and use the same one in the dev config's `GALLERY_PORT` and in `regenerate` |
| `regenerate` | the commands the page footer shows, the dev server with its port first; name the skill folder `<frontdoor-ui-gallery>`, since a reader may have it installed anywhere |
| `storageKey` | prefix of the browser storage that keeps reviews; unique per repository |
| `scale`, `quality` | device pixel ratio of the shots (2) and WebP quality (80); galleries of 20 to 50 states in two themes came to 2 to 4 MB at these values, and every re-render adds that again to the history |
| `defaults` | view keys applied to every view |
| `skipped` | states left out on purpose: `view`, the state's name, and `why` (unreachable, needs hardware, covered by another state); the page lists them under the view |

## A view

| Key | Meaning |
|---|---|
| `title`, `short` | section heading, and the shorter filter label |
| `size` | the window's width and height in CSS px, from the app's window config |
| `source`, `opens` | the component file, and how a user opens this window |
| `url` | path and query that select the view; the state is appended as `state=<scenario>`. A window with its own HTML entry uses that path (`/break.html`) |
| `scroller` | CSS selector of the element that scrolls, when it is not the document; a full-height shot grows the window until it no longer scrolls, title bars above it included |
| `themes` | `["light", "dark"]` by default; `["dark"]` for a view that has only one |
| `theme` | how the app picks its theme: `{"by": "media"}` (default, `prefers-color-scheme`), `{"by": "storage", "key": "app:theme", "values": {"light": "light", "dark": "dark"}}` (seeded into `localStorage` before the app starts), or `{"by": "script", "code": "..."}` (runs before the app with `THEME` set) |
| `clock` | local time, as ISO without a zone (`2026-10-22T09:00:00`), that `Date` reports, for greetings, dates and countdowns |
| `timers` | `"paused"` to run the page on a paused fake clock: `setTimeout`, `setInterval` and animation frames advance only by each wait's length, so a poll or a timeout that clears a message fires at the same moment in every run. Mock delays count too: keep each wait longer than the scenario's `delayMs` |
| `reducedMotion` | `true` to emulate reduced motion, for animations that never settle |
| `omitBackground` | `true` for a transparent window; the shot keeps its alpha |
| `settle` | ms to wait after load before the actions (700) |

A state may override `size`, `url`, `scroller`, `themes`, `clock`, `timers`, `settle`, `reducedMotion` and `omitBackground`, for example a window the app resizes to the whole screen in one mode. When the two sizes are two modes a user tells apart (a full-screen overlay and a corner card), two views with the same `url` read better on the page.

## A state

| Key | Meaning |
|---|---|
| `id` | unique; names the image files, so keep it short and stable |
| `view`, `state` | the view key, and the scenario name the mocks read from `?state=` |
| `title`, `how` | what the state is, and how a user gets there, in a sentence |
| `note` | a confirmed observation, or absent |
| `actions` | the steps that reach the state, in order (below); each may carry `"wait"` in ms (450) and `"label"`, the text the page shows for it. After the last step the pointer is moved off the page, so a hover style is not shot as part of the state |
| `keepHover` | `true` to leave the pointer where the last step put it, for a hover state |
| `crop` | `"window"` (default), `"full"` (the scroll height, with the window's fold marked on the page), or `{"selector": "section.card", "heading": "h2", "text": ["Portainer", "Danger zone"], "pad": 12}`: the union of the elements whose heading starts with one of the texts |

Actions:

| Step | Does |
|---|---|
| `{"click": "Save"}` | clicks the control with that accessible name; `"role"` defaults to `button` (`checkbox`, `radio`, `tab`, `link`, `switch` ...) |
| `{"fill": "Username", "value": "admin"}` | types into the field with that label |
| `"within": "<css>"`, `"nth": 1` | added to a click or fill: look only inside that element, or take the second match; needed when two controls share a name |
| `{"selector": "#autostart"}` | clicks the element a CSS selector finds; with `"value"` it types into it. For a control with no accessible name; give it a `label` |
| `{"hover": "Start"}` | rests the pointer on that control; set `"keepHover": true` on the state, or the pointer is moved off the page before the shot |
| `{"press": "Escape"}` | presses a key |
| `{"eval": "<js>"}` | runs a script in the page; the last resort, always with a `label` |

A value typed into a password field is a placeholder; never a real password.

## A real reference

`id` names `real/<id>.png`, `pair` names the state the page shows beside it, `view` and `title` label it. Render again after adding one; a missing file is left out with a warning.
