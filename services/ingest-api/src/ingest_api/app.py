import asyncio
from collections.abc import Awaitable, Callable

from fastapi import FastAPI
from fastapi.responses import JSONResponse


def create_app(readiness_checks: list[Callable[[], Awaitable[bool]]]) -> FastAPI:
    """Create and configure the ingest API application."""
    app = FastAPI(title="Ingest API")

    @app.get("/livez")
    async def livez() -> dict[str, bool]:
        """Report whether all configured readiness checks pass."""

        # Stop at the first failed check so unhealthy dependencies are reported promptly.
        for check in readiness_checks:
            if not await check():
                return {"ready": False}

        # All readiness checks passed.
        return {"ready": True}

    @app.get("/readyz")
    async def readyz() -> JSONResponse:
        """Report whether all configured readiness checks pass."""
        error_response = JSONResponse(
            status_code=503,
            media_type="application/problem+json",
            content={
                "type": "about:blank",
                "title": "Gateway Timeout",
                "status": 503,
            },
        )
        # Stop at the first failed check so unhealthy dependencies are reported promptly.
        try:
            async with asyncio.timeout(0.8):
                results = await asyncio.gather(*(task() for task in readiness_checks))
            if all(results):
                # All readiness checks passed.
                return JSONResponse(
                    status_code=200,
                    media_type="application/problem+json",
                    content={
                        "type": "about:blank",
                        "title": "success",
                        "status": 200,
                    },
                )
            return error_response
        except TimeoutError:
            return error_response

    return app
