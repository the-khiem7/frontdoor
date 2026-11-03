// Shared helpers for the gallery mocks. Copy into the repository's gallery
// folder, formatted with the repository's formatter; drop the comments where
// the repository forbids them.

/** The scenario this page shows, from ?state=<name>. */
export const stateName = new URLSearchParams(location.search).get("state") ?? "";

/** How the mocked calls of one scenario behave, by "<module>.<function>". */
export interface Behaviour {
  /** Calls that reject, with the error text the real backend would give. */
  fail?: Record<string, string>;
  /** Calls that never settle, to hold a busy or loading state on screen. */
  hang?: string[];
  /** Delay before a call settles, in ms; long enough to see a spinner, short enough to settle before the shot. */
  delayMs?: number;
  /**
   * What a failed call rejects with: an Error carrying the text (Wails, fetch
   * clients), or the bare string (Tauri `invoke` with a `Result<_, String>`).
   * Match the real backend, because the UI often prints `String(err)`.
   */
  rejectWith?: "error" | "string";
}

/** Returns a call() that resolves, rejects or hangs as the behaviour says. */
export function caller(b: Behaviour) {
  const delay = b.delayMs ?? 150;
  return function call<T>(name: string, value: T | (() => T)): Promise<T> {
    if (b.hang?.includes(name)) return new Promise<T>(() => {});
    const failure = b.fail?.[name];
    if (failure !== undefined) {
      const reason = b.rejectWith === "string" ? failure : new Error(failure);
      return new Promise<T>((_, reject) => setTimeout(() => reject(reason), delay));
    }
    return new Promise<T>((resolve) =>
      setTimeout(() => resolve(typeof value === "function" ? (value as () => T)() : value), delay),
    );
  };
}

/**
 * The type of a mock for every exported function of a real module. Write a
 * mock as `const mock = { ... } satisfies Mocked<typeof Real>` with
 * `import type * as Real from "<real module>"`: a function added to or changed
 * in the real module then fails the type check instead of the gallery. For a
 * platform module the app uses only part of, name those functions:
 * `Mocked<Pick<typeof Real, "listen">>`.
 */
export type Mocked<T> = {
  [K in keyof T]: T[K] extends (...args: infer A) => PromiseLike<infer R>
    ? (...args: A) => Promise<R>
    : T[K] extends (...args: infer A) => infer R
      ? (...args: A) => R
      : T[K];
};
