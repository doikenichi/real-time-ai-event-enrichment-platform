# Tasks

## 1. Spec
- [ ] 1.1 Add the "unknown" scenario; `openspec validate add-dashboard-service-status --strict` passes

## 2. Tests (red)
- [ ] 2.1 Vitest and Testing Library are configured; the starter test runs and fails
- [ ] 2.2 Write the test for the "unknown" scenario

## 3. Code (green → refactor)
- [ ] 3.1 `components/service-status.tsx` with a typed `state` prop (`"ready" | "unavailable" | "unknown"`)
- [ ] 3.2 `pnpm exec tsc --noEmit` and `pnpm lint` are clean

## 4. Docs
- [ ] 4.1 `web/dashboard/README.md`: how to run, how to test, and what the component does
