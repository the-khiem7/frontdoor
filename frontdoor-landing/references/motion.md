# Motion and interactive figures

A landing page that only holds still pictures reads like a README with more padding. What made a page land in practice was a hero that is the product's own mechanism, drawn as vector shapes and animated, and driven by the visitor: they press the one button the product itself waits for, and watch the result happen. Rough directions without motion undersold every option; the user only chose once a direction moved.

## What to animate

- The hero is a figure of what the product does, in the repository's signature, not a video and not a decorative loop. Pick the one moment of the product's flow a stranger should see: input in a messy state, the step the product performs, the output in its clean state.
- Let the visitor drive it. A primary button starts the run, and the same action is clickable inside the figure when the figure draws a control. A reset button returns to the start. A run that plays itself is a screensaver; a run the visitor starts is a demo.
- Motion is honest. Animate only what the code does, with labels taken from the code and the README. When the product stops for a human (an approval, a confirmation), the animation stops there and waits for the click; it never autoplays past a step the product would not skip.
- Further sections may each carry a small figure of their own idea, animated when they enter the viewport. Keep every one readable as a still frame.

## How to build it

- Inline SVG with a `viewBox`, colors from the page's tokens so both themes work, and an accessible text alternative on the figure (`role="img"` with an `aria-label` that says what the run shows, or a visible caption). The SVG itself can be `aria-hidden` when the label carries its content.
- A small state machine: waiting, running, done, back to waiting on reset. Disable the start button while running and enable reset when done, so no state can be entered twice.
- The Web Animations API: `el.animate(keyframes, { duration, fill: "forwards", easing })` on an SVG `<g>`, with `offset` on the keyframes to pass through waypoints (along a track, around a corner). Keep every returned animation and every `setTimeout` id in arrays, and cancel both on reset; a reset that leaves a timer running restarts motion the visitor stopped.
- Do not mix a `transform` attribute and a WAAPI transform on the same element: the animation overrides the attribute and the element jumps. Position elements with the animation only (a one-frame animation for a static position), or remove the attribute before animating.
- An `aria-live="polite"` status line beside the figure narrates each step in words, so the run is understandable to a screen reader and to anyone who looks away.
- A wide figure keeps a minimum width of about 760 px inside a horizontally scrollable frame on a phone; give the frame `tabindex="0"`, or axe reports it as an unfocusable scrollable region.

## Reduced motion

`prefers-reduced-motion: reduce` is not a rare setting. On Windows, turning off Settings > Accessibility > Animation effects (or "Show animations in Windows") makes Edge and Chrome report it to every page, and many people turn it off for speed without thinking about websites. A page that answers "nothing moves" shows those visitors a hero with dead buttons.

Treat two kinds of motion differently:

| Motion | Examples | Under reduce |
|---|---|---|
| ambient: the visitor did not ask for it | autoplay intro, loops, pulsing hints, scroll reveals, parallax | off; show the meaningful state at once |
| visitor-started: a click asked for it | the hero run, a tab that redraws a figure, a replay | still runs, at about a third of the duration, once, no loop |

- Never hide a control under reduce, and never let one become a no-op. Every button must visibly change the page in both modes.
- The first view under reduce is already a meaningful state (the input waiting at the step, the figure fully drawn), never blank space waiting for an animation that will not come.
- Write the rule into the code once: `var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;`, then scale durations with it (`duration * (reduce ? .35 : 1)`) in the visitor-started path, and skip only the ambient path.

Rejected, with the reason:

- Stop all motion under reduce, jump to the end state and hide the controls: the visitor sees a button that does nothing and concludes the page is broken; this happened on a real page.
- Ignore the setting: ambient loops and large movement are what the setting exists to stop, and some visitors set it because motion makes them unwell.

## Check it

`shoot.py check <root> --click "<start>,<reset>"` clicks each selector in order with and without reduced motion and fails when a click changes nothing on screen. Run it on every control that drives a figure. Then open the page yourself with animation effects off and on, and click through once.
