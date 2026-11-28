"""Day 001 · Challenge A: tests for the service-health spec.

Each test is named after a scenario in
openspec/changes/add-service-health-probes/specs/service-health/spec.md.
These tests are RED until you implement `ingest_api.app.create_app`.
"""

import asyncio
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
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    )


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
@pytest.mark.asyncio
async def test_readiness_times_out_when_a_check_hangs() -> None:
    async def hangs() -> bool:
        """
        hangs forever
        asyncio.Event() starts unset. Its wait() pauses the function until someone sets the event. This test never sets it, so hangs() stays paused. The return True is there to show what the function would return if it resumed.
        """
        await asyncio.Event().wait()
        return True

    # Arrange: create a client with one passing check and the hanging check.
    async with client_for(ready, hangs) as client:
        loop = asyncio.get_running_loop()
        start = loop.time()

        # Act: give pytest a little longer than the spec's 25-second limit
        # so a broken app cannot leave the test waiting forever.
        async with asyncio.timeout(2):
            response = await client.get("/readyz")

        elapsed = loop.time() - start

    # Assert: check the response and the spec's time limit.
    assert response.status_code == 503
    assert response.headers["content-type"].startswith("application/problem+json")
    assert elapsed <= 1
