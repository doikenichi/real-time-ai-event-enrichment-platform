/**
 * Day 001 · drill B: the words the dashboard shows for each service state.
 * RED until you create `lib/service-state.ts`. Challenge B's component then imports it.
 */
import { describe, expect, test } from "vitest";

import { STATE_LABELS, type ServiceState } from "./service-state";

describe("service state labels", () => {
  test("a ready service is shown as healthy", () => {
    expect(STATE_LABELS.ready).toBe("Healthy");
  });

  test("a service that isn't ready is shown as unavailable", () => {
    expect(STATE_LABELS.unavailable).toBe("Unavailable");
  });

  test("every state has words, never just a colour", () => {
    const states: ServiceState[] = ["ready", "unavailable"];
    for (const state of states) {
      expect(STATE_LABELS[state].length).toBeGreaterThan(0);
    }
  });
});
