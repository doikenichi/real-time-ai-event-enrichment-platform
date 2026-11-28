# Answer sheet: Day 001, drill B (`CoffeeStatus`)

> Verified? Not run here (no Node test tools where this was written). Run `lab test b coffee` to confirm.

## The answer
`web/dashboard/practice/coffee-status.tsx`:
```tsx
type CoffeeStage = "brewing" | "ready";

const STAGE_WORDS: Record<CoffeeStage, string> = {
  brewing: "Brewing…",
  ready: "Ready",
};

type CoffeeStatusProps = {
  pot: string;
  stage: CoffeeStage;
};

export function CoffeeStatus({ pot, stage }: CoffeeStatusProps) {
  return (
    <p role="status" aria-label={pot}>
      {STAGE_WORDS[stage]}
    </p>
  );
}
```

## Line by line
- `type CoffeeStage = "brewing" | "ready"`: a **union of literal types**. Only these two strings are allowed.
- `Record<CoffeeStage, string>`: an object that must have **one entry for every stage**. Add `"empty"` to the union and this line becomes a type error until you add its words (**exhaustiveness**).
- `type CoffeeStatusProps`: the component's inputs. `{ pot, stage }: CoffeeStatusProps` **destructures** them.
- `role="status"`: an ARIA **live region**: screen readers announce its content when it changes.
- `aria-label={pot}`: gives the element its **accessible name**, which is what `getByRole("status", { name: "kitchen" })` matches.
- `{STAGE_WORDS[stage]}`: looks up the words for the current stage.

## Why this way
- A `Record` lookup instead of `if`/`switch`: shorter, and the compiler checks every stage is covered. A `switch` with a `never` check does the same for logic that's more than a lookup.
- `aria-label` instead of a visible name: fine for a drill. In a real UI, prefer a visible label linked with `aria-labelledby`, so sighted and screen-reader users see the same name.

## Common mistakes
- Using `string` for the stage: the tests still pass, but the compiler can't catch a typo like `"redy"`.
- Putting the name in a `className` or `id`: `getByRole(..., { name })` ignores those.
- Forgetting `export`: the test can't import the component.

## Check yourself
1. What error do you get if `STAGE_WORDS` misses a stage, and where does it appear?
2. Why does the test find the element by role and name instead of by CSS class?
