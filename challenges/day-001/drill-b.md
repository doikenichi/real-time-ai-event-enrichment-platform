# Practice drill B: a `CoffeeStatus` badge (≈10 min at your pace)

Warm-up for Challenge B. Same ideas (a component with props, a union type with a `Record`, finding elements by role and name), on a different problem, so the real challenge feels familiar. Not part of the product.

**Answer sheet:** `lab answer drill-b`, but only after you've tried, or after 15 minutes stuck.

## Setup (1 min)
Do this after `setup-b.sh` (Challenge B, step 1), because it needs the dashboard's test tools.
```bash
mkdir -p web/dashboard/practice
```
`practice/` folders are git-ignored: drills never ship.

## The failing test (copy it)
Create `web/dashboard/practice/coffee-status.test.tsx`:
```tsx
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { CoffeeStatus } from "./coffee-status";

describe("CoffeeStatus", () => {
  it("says the coffee is brewing", () => {
    render(<CoffeeStatus pot="kitchen" stage="brewing" />);
    expect(screen.getByRole("status", { name: "kitchen" }).textContent).toContain("Brewing…");
  });

  it("says the coffee is ready", () => {
    render(<CoffeeStatus pot="kitchen" stage="ready" />);
    expect(screen.getByRole("status", { name: "kitchen" }).textContent).toContain("Ready");
  });
});
```
Run `lab test b coffee`. **Expected:** red, because `./coffee-status` doesn't exist.

## Your turn
Create `web/dashboard/practice/coffee-status.tsx` so both tests pass:
1. a type `CoffeeStage` that allows only `"brewing"` and `"ready"`
2. a `Record` from each stage to its words
3. an exported `CoffeeStatus` component with props `pot` and `stage`, showing the words in an element with `role="status"`, named after the pot

**Done when:** `lab test b coffee` → 2 passed.

## Stretch (2 min)
Add `"empty"` to the union *before* adding its words. Read the TypeScript error in the editor: that's the compiler making you handle every stage. Then fix it.
