# Screenshots of the built app

The mocked render shows what the frontend draws; a screenshot of the built app shows the real window: its frame, its webview, its fonts and scrollbars. A few of the main views are enough to catch where the two differ.

## Windows

`scripts/real.ps1` finds a top-level window by its exact title and captures it with `PrintWindow` and `PW_RENDERFULLCONTENT`, which includes WebView2 content even when other windows cover it. With `-Hide <regex>` it paints over every UI Automation element whose name matches, for example account paths:

```
powershell -NoProfile -File <skill-dir>/scripts/real.ps1 -Window "App settings" -Out design/ui-gallery/real/real-settings.png -Hide '\\Users\\'
```

- The window must be open and not minimised. Open it the way a user does: a tray menu item, a button, or a second launch of an app that is single-instance (a second launch shows the first instance's window). An app without single-instance handling starts a second copy on a second launch, with its own timers and tray icon: never do that. When a UI Automation click is needed, find the control by name in the window and invoke it; never send keystrokes to whatever has focus.
- A tray icon hidden in the notification overflow is out of reach without driving the shell; when the window is not open and only that icon opens it, skip the shot and say so.
- A popup that hides when it loses focus may vanish when another window opens; capture it first.
- Toggling a setting to make a window appear changes the user's state: turn it back afterwards and say so in the report.
- Never stop or start services, distributions or containers to reach a state; shoot the state the app is in, and leave the rest to the mocks.
- Look at each PNG before using it. Painting covers only text the accessibility tree names; a path drawn inside an image or a canvas is not found, so crop it out or leave the shot out.
- Window titles of Wails and Tauri windows are the `Title` or `title` of the window config; a frameless popup still has one.

## macOS and Linux

Not covered by a script. On macOS `screencapture -l <window id>` captures one window; on Linux, `import -window <id>` from ImageMagick on X11. Neither path was run with this skill; say so in the report if you use one.
