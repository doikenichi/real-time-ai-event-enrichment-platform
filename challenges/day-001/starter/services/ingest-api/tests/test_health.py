"""Day 001 · Challenge A: tests for the service-health spec.

Each test is named after a scenario in
openspec/changes/add-service-health-probes/specs/service-health/spec.md.
These tests are RED until you implement `ingest_api.app.create_app`.
"""

from collections.abc import Awaitable, Callable

import httpx
import pytest

from ingest_api.app import create_app

# A readiness check is any async callable that returns True (ready) or False (not ready).
ReadinessCheck = Callable[[], Awaitable[bool]]


async def ready() -> bool:
    return True


async def not_ready() -> bool:
    return False


def client_for(*checks: ReadinessCheck) -> httpx.AsyncClient:
    app = create_app(readiness_checks=list(checks))
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")


@pytest.mark.asyncio
async def test_liveness_reports_alive_without_checking_dependencies() -> None:
    # Liveness must NOT depend on downstream services: even a failing check keeps /livez at 200.
    async with client_for(not_ready) as client:
        response = await client.get("/livez")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_readiness_is_ok_when_all_checks_pass() -> None:
    async with client_for(ready, ready) as client:
        response = await client.get("/readyz")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_readiness_is_unavailable_when_any_check_fails() -> None:
    async with client_for(ready, not_ready) as client:
        response = await client.get("/readyz")

    assert response.status_code == 503
    assert response.headers["content-type"].startswith("application/problem+json")


# TODO (your spec refinement): write the test for the scenario you add to the spec:
#   "a readiness check that hangs makes /readyz answer 503 within the time budget".
# Hint: a check that does `await asyncio.sleep(10)`, and an assertion on elapsed time.
