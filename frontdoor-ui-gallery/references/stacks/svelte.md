# Svelte 5

## Recognise it

`svelte` 5.x and `@sveltejs/vite-plugin-svelte` in `package.json`, `.svelte` files with runes (`$state`, `$derived`, `$effect`, `$props`).

## Find the states

- Template branches: `{#if}`, `{:else if}`, `{:else}`, `{#each}` (an empty list is a state), `{#await}` (pending, then, catch), `class:name={...}` and `disabled={...}`.
- Shared state in `.svelte.ts` modules (`export const live = $state(...)`) set from a first call and from events; component state in `let x = $state(...)`. Local state that only a click sets (an open panel, a confirmation step) is reached with `actions`.
- Error text: the `catch` blocks that store `err.message`; the text comes from the backend.

## Type-check the mocks

`svelte-check --tsconfig ./tsconfig.json` checks only what `tsconfig.json` includes: add the `gallery` folder to `include`. A mock written with `satisfies Mocked<typeof Real>` then fails the check when the real module gains, loses or changes a function.

## In a plain browser

Svelte mounts normally. A component that reads `location.search` for its view works as is; one that reads it once at module load needs a full page load per shot, which `shoot.py` does.
