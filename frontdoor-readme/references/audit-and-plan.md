# Audit and plan

## Choose a figure by what the reader needs

Start from the reader's question for each section, not from the shape of the text.

| The reader needs to... | Make it | Keep as text |
|---|---|---|
| feel what the project is, or grasp an idea at a glance | a scene: one illustrated story in the repository's signature | one or two sentences beside it |
| follow exact order, gates or branches | a diagram, labelled on the lines | the table of branches, if one helps |
| both | a scene as the main picture and the diagram inside `<details><summary>` below it | a short summary line |
| find one value (an option, a flag, a command) | nothing: a table | all of it |
| copy a command | nothing: a code block, never hidden | all of it |

A scene earns its place when it carries meaning the text would take a paragraph to give: a before and after, a transformation, the place the project lives in. A diagram earns its place when the relations are precise. When a picture would only restate the sentence beside it, leave the sentence. The test: remove the sentence and look at the picture; if it still says something the sentence did not (a feeling, a relation, a place), keep it.

Common shapes that suit a scene or a figure (examples of content, not styles to copy): a problem and its solution as a before and after; a set of situations ("when you have X, do Y") as a short story each; the parts a thing is made of; a family of commands grouped by who calls them; a hierarchy or routing between parts; a link to an external guide as a card.

## Where `<details>` fits

Use `<details><summary>` for material a reader may want but most will not need first: the step-by-step flow under a scene, a secondary table, a directory tree, a long reference, a status note. Keep the summary line informative so a reader knows what is inside. Never hide the install or the first usage command.

## The plan to show the user

1. The hero: greenfield, the chosen direction; brownfield, the existing banner kept or a replacement proposed, with the reason.
2. Section order, each marked: new scene, new diagram, restyled text, moved to `Reference`, moved to `<details>`, unchanged.
3. A table of images: file name, kind, what it shows, source text it replaces.
4. The fact list: each statement or command the README will make, and where in the repo it comes from. For a README written from nothing, this is the plan for the text.
5. What is lost: any text form that disappears, any duplicated truth created (a figure that restates a diagram kept elsewhere in the repo, with nothing comparing them).
6. Files that will be added or changed, the test or convention that could break, and the render cost (number of images, expected size).
7. Questions still open, with a recommendation for each.

## Checks that catch real mistakes

- Every statement in an image traces to the README or the code; a figure is where an invented claim hides.
- Examples inside an image use obviously fictional names so no one mistakes them for real entries.
- The reading order still works with images off: headings and alt text alone tell the story.
- The swap test: replace the project's name and text with another project's. If the pictures still fit, they are generic.
- A bug nobody sees until the page is open: the old text had a sentence that references labels the diagram no longer shows. Rewrite those sentences instead of copying them.
