# Answer sheet: Day 001, Challenge B (`ServiceStatus`)

> Verified? Not run here. Written against the starter tests plus an "unknown" scenario that shows "Checking…". Run `lab test b` to confirm; if you chose other words for "unknown", use yours.

## The answer
`web/dashboard/lib/service-state.ts` (from drill B, with `"unknown"` added in step 5):
```ts
export type ServiceState = "ready" | "unavailable" | "unknown";

export const STATE_LABELS: Record<ServiceState, string> = {
  ready: "Healthy",
  unavailable: "Unavailable",
  unknown: "Checking…",
};
```
`web/dashboard/components/service-status.tsx`:
```tsx
import { STATE_LABELS, type ServiceState } from "@/lib/service-state";

type ServiceStatusProps = {
  name: string;
  state: ServiceState;
};

export function ServiceStatus({ name, state }: ServiceStatusProps) {
  return (
    <p role="status" aria-label={name} data-state={state}>
      <span>{name}</span>: <strong>{STATE_LABELS[state]}</strong>
    </p>
  );
}
```
The added test, in `__tests__/service-status.test.tsx`:
```tsx
test("shows the state as unknown before the first result", () => {
  render(<ServiceStatus name="ingest-api" state="unknown" />);

  expect(screen.getByRole("status", { name: "ingest-api" }).textContent).toContain("Checking…");
});
```
And in `app/page.tsx`: `<ServiceStatus name="ingest-api" state="unknown" />` until real data arrives.

## Line by line
- `import … from "@/lib/service-state"`: the type and words come from drill B; `@/` is the import alias set up by `create-next-app` for the dashboard's root folder.
- `STATE_LABELS[state]`: the words for each state. **Words, not just colour** (WCAG 1.4.1): "Unavailable" is readable on any screen, in any colour scheme, by any user.
- `data-state={state}`: a hook for styling later (green, red, grey) without changing the text or the tests.
- `<span>{name}</span>: <strong>…</strong>`: the visible text names the service and its state, so sighted users see the same thing a screen reader announces.

## Why this way
- **The spec first, then the test, then the type:** adding `"unknown"` to the union makes `tsc` point at the `Record`, so the compiler guides the change.
- `role="status"` rather than `role="alert"`: a status is announced politely; an alert interrupts. A service going down is worth an alert later, in the incident view, not in every status badge.

## Common mistakes
- Hard-coding `"Healthy"` in JSX with a ternary: works for two states, gets messy at three, and the compiler can't check it's complete.
- Showing only a coloured dot: fails WCAG 1.4.1 and the "unknown" scenario.

## Check yourself
1. Which file would fail to compile if a fourth state were added to the union?
2. What's the difference between `role="status"` and `role="alert"` for a screen-reader user?
