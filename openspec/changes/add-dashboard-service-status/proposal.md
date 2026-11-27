# Add a service status indicator to the dashboard

## Why
Operators need to see at a glance whether each platform service is ready. This is the first building block of the live dashboard, and it will later be fed by `/readyz` and live events.

## What changes
- New `web/dashboard` Next.js app (App Router, strict TypeScript), the first member of the pnpm workspace
- Vitest and React Testing Library set up for component tests
- `ServiceStatus` component: shows a service's name and state as an accessible live status, never by colour alone

## Impact
- New capability: `dashboard-status`
- New code: `web/dashboard/`, `pnpm-workspace.yaml`
