# Vue 3

## Recognise it

`vue` 3.x and `@vitejs/plugin-vue` in `package.json`, `.vue` single-file components, usually `<script setup lang="ts">`.

## Find the states

- Template branches: `v-if`, `v-else-if`, `v-else`, `v-show` (present but hidden: shoot it shown and hidden), `v-for` over an empty list, `:disabled`, `:class` bindings that change the look.
- Data: `ref`, `reactive` and `computed` in the component, composables (`useX()`) and stores (Pinia `defineStore`). A composable that starts from a call and then follows events (a tick, a status push) shows its first state from the call; push one event from the mock when a state only exists after it.
- Polling: `setInterval(refresh, ms)` re-reads the backend all the time. The mocks must return the same data on every call; do not freeze or remove the timer.
- Several entries: an app may have several HTML entries (`index.html`, `break.html`), each mounting its own root component; each is a view with its own `url`.

## Type-check the mocks

`vue-tsc --noEmit` reads `tsconfig.json` (often split into `tsconfig.app.json` and `tsconfig.node.json`): add the `gallery` folder to the `include` of the app config. Types declared inside a component (`interface Status` in a `.vue` file) cannot be imported; type the scenarios with the wrapper's types or a types module when there is one, and say in the report which mocks are typed by hand.

## In the mocks

- An argument the app passes into a mock is often a reactive proxy: `structuredClone` throws `DataCloneError` on it. Copy it with `JSON.parse(JSON.stringify(x))` or `toRaw` before keeping it in the store.
- Number fields that share one label ("minutes" in every row) cannot be told apart by `fill`: scope the step with `within` or `nth`.

## In a plain browser

Vue mounts normally. A theme picked in `onMounted` from `localStorage` or `matchMedia` needs the view's `theme` set to `storage` or to the media default. A greeting or a date read from `new Date()` needs `clock`.
