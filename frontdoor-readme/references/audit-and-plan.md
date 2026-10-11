# Audit and plan

## Content to figure

| The README text is... | Make it... | Keep as text |
|---|---|---|
| a problem the product solves, before and after | a two-lane strip: without / with | one or two sentences under it |
| an ordered workflow with branches | a flow diagram with the decision labels on the lines | the comparison table of branches |
| a set of situations ("when you have X, do Y") | one strip per situation: situation, steps, result | nothing; the strip replaces the prose |
| the parts a thing is made of | a stacked cards figure with core and optional parts told apart | exact field syntax, in a code block |
| a family or catalogue of commands | a grouped map: who calls it, when, for what | the full table, in `<details>` if long |
| a hierarchy or routing between parts | a tree or hub figure with the dependency edges | the directory layout, in `<details>` |
| a link to an external guide | a card-shaped button with chips for what it covers | nothing |
| install or usage commands | nothing | all of it, as code blocks |

## The plan to show the user

1. Section order, each marked: new image, restyled text, moved to `Reference`, moved to `<details>`, unchanged.
2. A table of images: file name, kind, what it shows, source text it replaces.
3. What is lost: any text form that disappears, any duplicated truth created (a figure that restates a diagram kept elsewhere in the repo, with nothing comparing them).
4. Files that will be added or changed, the test or convention that could break, and the render cost (number of images, expected size).
5. Questions still open, with a recommendation for each.

## Checks that catch real mistakes

- Every statement in an image traces to the README or the code; a figure is where an invented claim hides.
- Examples inside an image use obviously fictional names so no one mistakes them for real entries.
- The reading order still works with images off: headings and alt text alone tell the story.
- A bug nobody sees until the page is open: the old text had a sentence that references labels the diagram no longer shows. Rewrite those sentences instead of copying them.
