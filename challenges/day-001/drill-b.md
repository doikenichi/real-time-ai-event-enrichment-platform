# Practice drill B: the words for each service state (≈10 min at your pace)

Warm-up for Challenge B, and a real piece of the dashboard: the map from a service's state to the words it shows. Challenge B's `ServiceStatus` component then imports it, so this drill shortens the challenge.

**Concepts:** union types and `Record` (the same as in the challenge), plus a first plain Vitest test, without React.
**Answer sheet:** `lab answer drill-b`, but only after you've tried, or after 15 minutes stuck.

## Setup (0 min)
Run `bash challenges/day-001/setup-b.sh` first (Challenge B, step 1). It also copies this drill's failing test to `web/dashboard/lib/service-state.test.ts`.

Run `lab test b service-state`. **Expected:** red, because `./service-state` doesn't exist.

## Your turn
Create `web/dashboard/lib/service-state.ts` that exports:
1. a type `ServiceState` that allows only `"ready"` and `"unavailable"`
2. a constant `STATE_LABELS`: a `Record` from each state to the words the tests expect

**Done when:** `lab test b service-state` → 3 passed. **Commit:** `lab save "service state labels"`

## Stretch (2 min)
Add `"unknown"` to the union *before* adding its words, and read the TypeScript error in the editor: the compiler won't let a state exist without words. Undo it for now; Challenge B, step 5, adds `"unknown"` test-first.

## How Challenge B uses it
In step 4 of `guide-b.md`, import `STATE_LABELS` and `ServiceState` from `@/lib/service-state` instead of writing them inside the component.
