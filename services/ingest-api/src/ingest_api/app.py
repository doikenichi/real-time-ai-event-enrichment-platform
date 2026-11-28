from collections.abc import Awaitable, Callable

from fastapi import FastAPI


def create_app(readiness_checks: list[Callable[[], Awaitable[bool]]]) -> FastAPI:
    """Create and configure the ingest API application."""
    app = FastAPI(title="Ingest API")

    @app.get("/livez")
    async def livez() -> dict[str, bool]:
        return {"alive": True}

    return app
