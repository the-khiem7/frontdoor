// Template: the scenarios of one app. Copy beside mock-kit.ts as fixtures.ts,
// replace the example types and data with the app's own, and delete what the
// app does not need. Each scenario is the data the backend would return in
// one state; the page picks one with ?state=<name>.
import { caller, stateName, type Behaviour, type Mocked } from "./mock-kit";
// import type { Status, Settings } from "<the app's own types or generated models>";

type Status = { phase: "running" | "stopped"; version: string; error?: string };
type Settings = { autostart: boolean };

export interface Scenario extends Behaviour {
  status?: Partial<Status>;
  settings?: Partial<Settings>;
  /** Path a file picker returns. */
  pick?: string;
}

// The typical state; every scenario changes only what differs from it.
export const baseStatus: Status = { phase: "running", version: "1.2.3" };
export const baseSettings: Settings = { autostart: true };

export const scenarios: Record<string, Scenario> = {
  running: {},
  stopped: { status: { phase: "stopped" } },
  "start-failed": { status: { phase: "stopped" }, fail: { "Service.Start": "timed out waiting for the service" } },
  "settings-loading": { hang: ["Settings.Get"] },
};

export const scenario: Scenario = scenarios[stateName || "running"] ?? {};
export const call = caller(scenario);

/**
 * State that a command changes. A success state is only believable when the
 * screen around the notice agrees with it: after Save, a reload must return
 * what was saved. Keep that state here, in memory, starting from the scenario
 * on every page load, so each shot is still the same in every run.
 */
export const store = {
  settings: { ...baseSettings, ...scenario.settings },
};

export type { Mocked };
