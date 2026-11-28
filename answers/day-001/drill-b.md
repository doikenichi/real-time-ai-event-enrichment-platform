# Answer sheet: Day 001, drill B (the words for each service state)

> Verified? Not run here (no Node test tools where this was written). Run `lab test b service-state` to confirm.

## The answer
`web/dashboard/lib/service-state.ts`:
```ts
export type ServiceState = "ready" | "unavailable";

export const STATE_LABELS: Record<ServiceState, string> = {
  ready: "Healthy",
  unavailable: "Unavailable",
};
```

## Line by line
- `export type ServiceState = "ready" | "unavailable"`: a **union of literal types**: only these two strings are allowed. `export` lets the component (and the tests) use the same type.
- `Record<ServiceState, string>`: an object that must have **one entry for every state**. Add `"unknown"` to the union and this line becomes a type error until you add its words (**exhaustiveness checking**).
- The file has no React in it: it's plain data, so it's easy to test and to reuse (for example, in a notification later).

## Why this way
- **Separate the words from the component:** the component decides how things look; this file decides what they're called. That's **separation of concerns**, and it lets you change wording (or translate it, **i18n**) without touching the component.
- A `Record` lookup instead of `if`/`switch`: shorter, and the compiler checks every state is covered. A `switch` with a `never` check does the same when there's more logic than a lookup.
- `as const` objects plus `keyof typeof` are another common way to get the same type from the data. Starting from the union is clearer when the states come from a spec.

## Common mistakes
- Using `string` for the state: the tests still pass, but the compiler can't catch a typo like `"redy"`.
- Forgetting `export` on the type: the test's `import { type ServiceState }` fails.
- Words with different capitals from the test ("healthy"): `toBe` compares exactly.

## Check yourself
1. What error do you get if `STATE_LABELS` misses a state, and where does it appear?
2. Why is this file easier to test than the component?
