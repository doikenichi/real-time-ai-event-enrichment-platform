# Guide for Challenge A: health probes, one tiny step at a time

This guide turns Challenge A into small steps. Each step teaches **one** idea, shows it on a *different* example, then asks you to apply it. After every step you run a command and compare what you see with the expected result.

**Rules of the game**
- Do the steps in order. Don't read ahead to the answers.
- When a step's check passes, commit. Small commits are the point of TDD.
- Stuck for more than 5 minutes? Open the hints one at a time. Still stuck after the last hint? Ask Claude or Codex *"explain step N of guide-a, don't give me the code"*. They follow the rules in `AGENTS.md` and will coach you.
- Typing the examples yourself, instead of copying them, helps you remember them.

Time: about 45–60 minutes the first time. That's fine; it gets faster.

---

## Step 0: What are we building, and what is TDD? (5 min, reading)

**The service.** `ingest-api` is a small web service. Kubernetes (later) asks every service two questions over HTTP:
- `GET /livez`: *"Are you alive?"* Answer `200` if the process is running. Don't check anything else.
- `GET /readyz`: *"Can you take traffic right now?"* Ask each dependency (Kafka, the database and so on) whether it's OK. Answer `200` if all are, `503` ("Service Unavailable") if any isn't.

**TDD (test-driven development)** is a loop:
1. **Red:** run a test that fails, because the code doesn't exist yet.
2. **Green:** write the *simplest* code that makes that test pass. Ugly is fine.
3. **Refactor:** improve the code while the tests stay green.

The tests are already written for you in `services/ingest-api/tests/test_health.py`. Open it and read it now. You don't need to understand every line yet. Notice:
- Each `async def test_...` is one test, named after a scenario in the spec.
- `client_for(ready, not_ready)` builds the app with two fake dependency checks: one that says "OK", one that says "not OK".
- `assert response.status_code == 200` is the expectation.

**Useful commands**
| Command | What it does |
|---|---|
| `uv run --package ingest-api pytest services/ingest-api -q` | runs all the tests |
| `... -q -k liveness` | runs only the tests whose name contains `liveness` |
| `git add -A && git commit -m "day-001: <what now works>"` | saves a step |

---

## Step 1: Create the workspace and see red (10 min)

**Idea: a workspace** is one repo holding several projects. The root `pyproject.toml` lists them; `uv` installs everything into one shared environment.

Run these one at a time, from the repo root, inside the dev container:
```bash
uv init --bare --name platform .
```
This creates `pyproject.toml` at the root. (Already have a root `pyproject.toml` from the setup? Then skip this command; it's there.) Open it in the editor and add these two lines at the end:
```toml
[tool.uv.workspace]
members = ["services/*"]
```
They mean: "every folder inside `services/` is a project of this workspace".

```bash
uv init --package --name ingest-api services/ingest-api
```
This creates `services/ingest-api/` with `src/ingest_api/__init__.py`. Python package names use `_` where the project name uses `-`.

```bash
uv add --package ingest-api fastapi
uv add --package ingest-api --dev pytest pytest-asyncio httpx ruff mypy
cp -r challenges/day-001/starter/services/ingest-api/tests services/ingest-api/
uv run --package ingest-api pytest services/ingest-api -q
```

**Expected:** an error that mentions `ModuleNotFoundError: No module named 'ingest_api.app'`. That's **red**, and it's the right red: the test is looking for code you haven't written.

**Commit:** `day-001: failing tests for service health`

<details><summary>Hint: "uv add" fails while building pydantic-core</summary>A library may not have ready-made packages for Python 3.15 yet. Run <code>uv python pin 3.14</code>, then repeat the <code>uv add</code> commands, and write it down for tomorrow's review.</details>

---

## Step 2: Make the import work (5 min)

**Idea: reading errors is progress.** In TDD, the error message tells you what to do next. Right now it says the module `ingest_api.app` doesn't exist, so create it.

**Idea: an app factory** is a function that *builds and returns* the app, instead of one global app. Tests can then build a fresh app with whatever fakes they want.

**Example (a different app, to learn the shape):**
```python
# greeter/app.py
from fastapi import FastAPI


def create_greeter(name: str) -> FastAPI:
    app = FastAPI()
    return app
```
- `def create_greeter(name: str) -> FastAPI:` defines a function. `name: str` says the argument is a string; `-> FastAPI` says what it returns. These are **type hints**; `mypy` checks them later.

**Your turn:** create `services/ingest-api/src/ingest_api/app.py` with a function `create_app` that takes one argument, `readiness_checks`, and returns a `FastAPI` app with no routes yet. For the type hint of `readiness_checks`, look at how the test file describes a check (`ReadinessCheck`) and copy that idea.

**Check:** run the tests. **Expected:** no more import error. Now the 3 tests *fail* with `404` (not found), because the routes don't exist yet. A different red means progress.

<details><summary>Hint 1</summary>The test calls <code>create_app(readiness_checks=list(checks))</code>, so the parameter must be called exactly <code>readiness_checks</code>.</details>
<details><summary>Hint 2: the type</summary>A check is "a function with no arguments that you can <code>await</code>, which gives a <code>bool</code>". In Python types that's <code>Callable[[], Awaitable[bool]]</code>, imported from <code>collections.abc</code>. The argument is a <code>list</code> of those. Give it a name: <code>ReadinessCheck = Callable[[], Awaitable[bool]]</code>.</details>

---

## Step 3: Green for `/livez` (5 min)

**Idea: a route** connects a URL to a function. FastAPI calls the function when that URL is requested, and turns what it returns into the HTTP response (a `dict` becomes JSON, with status `200`).

**Idea: `async def`** makes a function that can wait without blocking the others. Web frameworks call your route with `await`.

**Example:**
```python
def create_greeter(name: str) -> FastAPI:
    app = FastAPI()

    @app.get("/hello")
    async def hello() -> dict[str, str]:
        return {"message": f"hello {name}"}

    return app
```
- `@app.get("/hello")` is a **decorator**: it registers the function below it as the handler for `GET /hello`.
- The route is defined *inside* the factory, so it can use `name`. That's how the factory "injects" values.

**Your turn:** add a `/livez` route that returns something small, like a status of "alive". Don't touch `readiness_checks` here: liveness must not check dependencies.

**Check:** `uv run --package ingest-api pytest services/ingest-api -q -k liveness` → **1 passed**. That's your first green.

**Commit:** `day-001: liveness probe`

---

## Step 4: Green for `/readyz` when everything is OK (10 min)

**Idea: dependency injection.** `create_app` doesn't know *what* the checks are (Kafka? a database?). It only knows each one is a function it can await. Tests pass fakes; production will pass real ones. You can test the logic without starting Kafka. This is the **port** the README mentions: an interface the app depends on, with replaceable implementations.

**Idea: calling and awaiting a check.** `check` is the function; `check()` calls it and gives an awaitable; `await check()` waits for it and gives the `bool`.

**Example (simplest version: one at a time):**
```python
async def everyone_is_coming(friends: list[Callable[[], Awaitable[bool]]]) -> bool:
    for ask in friends:
        if not await ask():
            return False
    return True
```

**Your turn:** add a `/readyz` route that awaits each readiness check and returns status `200` when all of them say `True`. Keep it simple: a loop is fine for now. Don't handle the failure case yet.

**Check:** `... -k "readiness_is_ok"` → **1 passed**.

**Commit:** `day-001: readiness ok when all checks pass`

---

## Step 5: Green for `/readyz` when something is wrong (10 min)

**Idea: choosing the status code.** Returning a `dict` always gives `200`. To answer `503`, return a response object where you set the code yourself.

**Idea: problem details (RFC 9457)** is the standard JSON shape for HTTP errors, with the media type `application/problem+json`. The minimal fields are `type`, `title` and `status`. Don't put internal details (stack traces, hostnames, which dependency failed) in it: attackers read error messages too.

**Example:**
```python
from fastapi.responses import JSONResponse


@app.get("/teapot")
async def teapot() -> JSONResponse:
    return JSONResponse(
        status_code=418,
        content={"type": "about:blank", "title": "I'm a teapot", "status": 418},
        media_type="application/problem+json",
    )
```

**Your turn:** when any check says `False`, make `/readyz` return `503` as problem details. When all pass, return `200`. Tip: if the route can return two different things, it's easier for `mypy` if both are a `JSONResponse`.

**Check:** run **all** tests → **3 passed**.

**Commit:** `day-001: readiness unavailable when a check fails`

<details><summary>Hint</summary>Use the <code>for</code> loop from step 4. As soon as one check is <code>False</code>, return the 503 response. After the loop, return the 200 one.</details>

---

## Step 6: Refactor to run the checks at the same time (10 min)

**Idea: refactor** means changing how code works without changing what it does. The tests prove you didn't break anything: they must stay green.

**Idea: concurrency.** Your loop asks the checks one after another. If each takes 1 second, three checks take 3 seconds. Running them **concurrently** is like putting three kettles on at once: the total is about as long as the slowest one.

**Example:**
```python
import asyncio


async def boil_kettle() -> bool: ...
async def toast_bread() -> bool: ...


results = await asyncio.gather(boil_kettle(), toast_bread())  # a list: [True, True]
```
- `asyncio.gather(a(), b())` runs both and waits until both are done. It returns their results in a list, in order.
- With a list of functions, build the calls with a **generator** and *unpack* it with `*`: `asyncio.gather(*(task() for task in tasks))`.
- `all(results)` is `True` only if every value is `True`.

**Your turn:** replace the loop in `/readyz` with `asyncio.gather` and `all`.

**Check:** all tests → still **3 passed**.

**Commit:** `day-001: run readiness checks concurrently`

(The README also mentions `asyncio.TaskGroup`, a newer alternative to `gather`. `gather` is easier to start with; tomorrow's review compares them.)

---

## Step 7: A hung dependency must not hang the probe (15 min)

This step is a full red → green cycle that you write yourself.

**First, the spec.** Open `openspec/changes/add-service-health-probes/specs/service-health/spec.md`. Copy the shape of an existing scenario and add: *"readiness is unavailable when a check hangs"*. Choose a time budget, for example 1 second, and write it in the scenario. Then run `openspec validate add-service-health-probes --strict`.

**Then the red test.** Add it to the test file. Fill in the `...`:
```python
import asyncio
import time


async def hangs() -> bool:
    await asyncio.sleep(10)  # pretends to be a dependency that never answers
    return True


@pytest.mark.asyncio
async def test_readiness_is_unavailable_when_a_check_hangs() -> None:
    started = time.perf_counter()
    async with client_for(hangs) as client:
        response = await client.get("/readyz")
    elapsed = time.perf_counter() - started

    assert response.status_code == ...
    assert elapsed < ...
```
Run it. **Expected:** it fails, after about 10 seconds. That's the bug the test catches.

**Commit:** `day-001: failing test for a hanging readiness check`

**Idea: a timeout** cancels the waiting after a budget and raises `TimeoutError`, which you can catch.

**Example:**
```python
try:
    async with asyncio.timeout(1.0):
        await download_file()
except TimeoutError:
    print("too slow, giving up")
```

**Your turn:** wrap your `gather` in `asyncio.timeout(...)` with your budget. When it times out, answer like any other "not ready". Put the budget in a named constant, not a bare number.

**Check:** all tests → **4 passed**, and the run takes about 1 second, not 10.

**Commit:** `day-001: readiness probe times out hung checks`

---

## Step 8: Make the quality tools happy (10 min)

| Tool | What it checks | Auto-fix |
|---|---|---|
| `uv run ruff check` | common mistakes and style (unused imports and so on) | `uv run ruff check --fix` |
| `uv run ruff format --check` | layout (spaces, line length) | `uv run ruff format` |
| `uv run mypy --strict services/ingest-api/src` | type hints: every function says what it takes and returns | none: you fix the hints |

Run the auto-fixes first, then the checks. For each `mypy` error:
1. Read the line number and the message.
2. Most first-day errors are *"Function is missing a return type annotation"*: add `-> ...` to that function.

**Check:** all three commands print no errors, and the tests still pass.

**Commit:** `day-001: lint and type checks clean`

Then do the Docs step from the README (ADR-0005).

---

## Glossary
| Term | Meaning |
|---|---|
| **probe** | an HTTP endpoint that a platform calls to check a service |
| **liveness / readiness** | "is the process alive?" / "can it serve traffic now?" |
| **async, await** | a way to wait for slow things (network) without blocking everything else |
| **app factory** | a function that builds and returns the app, so tests can build their own |
| **dependency injection** | passing collaborators in (here, the checks) instead of creating them inside |
| **port and adapter** | the interface the app needs (a check) and its real or fake implementations |
| **fake** | a simple stand-in used by tests (`ready`, `not_ready`) |
| **concurrency** | several waits overlapping in time |
| **timeout** | a maximum time to wait before giving up |
| **problem details (RFC 9457)** | the standard JSON format for HTTP errors |
| **type hint** | a label for what a variable or function takes and returns |

## Learn more (optional, short)
- FastAPI tutorial: [First steps](https://fastapi.tiangolo.com/tutorial/first-steps/) and [Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- Python docs: [Coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html) (read "Coroutines", "Running tasks concurrently" and "Timeouts")
- Fluent Python (2nd ed.), ch. 21, "Asynchronous Programming"
