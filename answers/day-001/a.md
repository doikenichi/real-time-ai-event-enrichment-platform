# Answer sheet: Day 001, Challenge A (health probes)

> Verified? Written to pass the starter tests plus the "hung check" test from guide-a, step 7. Not run here (FastAPI isn't installed where this was written). Run `lab test a` to confirm.

## The answer
`services/ingest-api/src/ingest_api/app.py`:
```python
import asyncio
from collections.abc import Awaitable, Callable, Sequence

from fastapi import FastAPI
from fastapi.responses import JSONResponse

ReadinessCheck = Callable[[], Awaitable[bool]]

READINESS_TIMEOUT_SECONDS = 1.0


async def all_ready(checks: Sequence[ReadinessCheck]) -> bool:
    """True only if every check answers True within the time budget."""
    try:
        async with asyncio.timeout(READINESS_TIMEOUT_SECONDS):
            results = await asyncio.gather(
                *(check() for check in checks), return_exceptions=True
            )
    except TimeoutError:
        return False
    return all(result is True for result in results)


def create_app(readiness_checks: Sequence[ReadinessCheck]) -> FastAPI:
    app = FastAPI(title="ingest-api")

    @app.get("/livez")
    async def livez() -> dict[str, str]:
        return {"status": "alive"}

    @app.get("/readyz")
    async def readyz() -> JSONResponse:
        if await all_ready(readiness_checks):
            return JSONResponse({"status": "ready"})
        return JSONResponse(
            status_code=503,
            media_type="application/problem+json",
            content={
                "type": "about:blank",
                "title": "Service Unavailable",
                "status": 503,
            },
        )

    return app
```

## Line by line
- `ReadinessCheck = Callable[[], Awaitable[bool]]`: a **type alias**. A check is "a function with no arguments that you can await, and that gives a bool". Naming it makes the signatures readable.
- `READINESS_TIMEOUT_SECONDS = 1.0`: a **named constant** instead of a bare number in the code. The spec scenario says the budget, so the code says it too.
- `all_ready(...)`: the readiness logic, pulled out of the route so it can be read (and later tested) on its own.
- `asyncio.timeout(...)`: cancels everything inside the `async with` block if it takes longer than the budget, and raises `TimeoutError`.
- `asyncio.gather(*(check() for check in checks), ...)`: starts every check at once and waits for all of them. The `*` unpacks the generator into separate arguments.
- `return_exceptions=True`: a check that **crashes** gives back its exception instead of crashing the probe. A crashing dependency is "not ready", not a 500 error.
- `all(result is True for result in results)`: ready only if every result is exactly `True` (an exception object isn't).
- `livez` returns a constant: **liveness never checks dependencies**. If it did, a Kafka outage would make Kubernetes restart every healthy pod (a restart storm).
- The 200 answer is plain JSON (`application/json`); only **errors** use `application/problem+json`.
- The 503 body has no internal details (no dependency names or messages), so it leaks nothing to attackers.

## Why this way
| Choice | Alternative | Trade-off (industry terms) |
|---|---|---|
| `asyncio.gather` | `asyncio.TaskGroup` (**structured concurrency**, Python 3.11+) | `TaskGroup` cancels the other checks as soon as one fails, which is cleaner for many checks, but it needs coroutines (`Coroutine` types) and `except*` for its `ExceptionGroup`. `gather` is simpler for a first version. |
| one budget for all checks | a timeout per check | per-check timeouts let a report say which check was slow (later, for a detailed localhost-only view); one budget is what the probe needs. |
| constant in the module | a setting (environment variable, Pydantic Settings) | **twelve-factor config**: later, the budget comes from configuration, with this as the default. |

## Common mistakes (and what catches them)
- Running the dependency checks in `/livez` too: not caught by today's tests, but it breaks the liveness/readiness contract. A test "liveness ignores failing checks" would catch it (`client_for(not_ready)` → `/livez` still 200).
- Returning `application/problem+json` for a **successful** 200: problem details are for errors only.
- A 503 titled "Gateway Timeout": that's 504's name. The RFC 9457 `title` should match the status: "Service Unavailable".
- A bare `0.8` in the code: name it, and put the same number in the spec scenario.
- `await asyncio.gather(...)` **without** a timeout: the hung-check test runs for 10 seconds and fails.

## Check yourself
1. Why must `/livez` not await the readiness checks?
2. What happens to a check that raises an exception, with and without `return_exceptions=True`?
3. What would you change to report *which* check timed out, only to requests from localhost?
