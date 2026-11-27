/**
 * Day 001 · Challenge B: tests for the dashboard-status spec.
 *
 * Each test is named after a scenario in
 * openspec/changes/add-dashboard-service-status/specs/dashboard-status/spec.md.
 * RED until you create `components/service-status.tsx`.
 */
import { render, screen } from "@testing-library/react";
import { describe, expect, test } from "vitest";

import { ServiceStatus } from "../components/service-status";

describe("ServiceStatus", () => {
  test("shows the service as healthy when it is ready", () => {
    render(<ServiceStatus name="ingest-api" state="ready" />);

    expect(screen.getByRole("status", { name: "ingest-api" }).textContent).toContain("Healthy");
  });

  test("shows the service as unavailable when it is not ready", () => {
    render(<ServiceStatus name="ingest-api" state="unavailable" />);

    expect(screen.getByRole("status", { name: "ingest-api" }).textContent).toContain("Unavailable");
  });

  // TODO (your spec refinement): add the "unknown" scenario to the spec first, then its test.
  // Status must never be conveyed by colour alone (WCAG 1.4.1).
});
