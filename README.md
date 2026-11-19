
# AdvisoryAtlas

AdvisoryAtlas answers the question "Am I affected?" using CERT-In advisories and vulnerability notes. It identifies the affected product versions, provides the relevant note ID, and explains the recommended fix.

**Status:** Day 1 foundation (FastAPI skeleton, quality gates). Live URL from Day 5.

## Who it's for

IT administrator at a 300-bed private hospital in Coimbatore who must patch Windows servers, Fortinet firewalls and a hospital information system on time.

## The problem

Hospitals depend on multiple software products, servers and network devices to deliver their services. CERT-In publishes vulnerability notes and advisories, but administrators may struggle to identify which notices affect the exact versions running in their hospital. They need a faster way to check whether a product is affected and understand what action is required. AdvisoryAtlas aims to make this process easier by matching product versions against published vulnerability information.

## Data sources

CERT-In vulnerability notes and advisories for the last 3+ years, plus CERT-In Directions of 28 April 2022 and their FAQs.

- https://www.cert-in.org.in/ (menus: Advisories, Vulnerability Notes)
- Terms: Public government notices. Cite the note ID. Download slowly (1 request every 2 seconds).

## Hardest problem (my interview story)

Version-range matching: 'FortiOS 7.0.0 through 7.0.12 affected' must match a user on 7.0.11 but not one on 7.2.1. Retrieval finds the note, but 'affected or not' must come from parsed version ranges compared in code (packaging.version), never from the LLM.

## Signature feature

My-stack checker: register products and versions once and see every matching note with an Affected / Not affected / Check manually badge.

## Target metric

Affected/not-affected correctness of 90%+ on 40 product-version test cases.

## Run it locally

```bash
uv sync
cp .env.example .env
# Windows: copy .env.example .env
uv run uvicorn advisoryatlas.api.main:create_app --factory --reload
```

Then open http://localhost:8000/docs

## Checks

```bash
uv run pytest
uv run ruff check .
```

Run the integration tests against the Compose Postgres:

```bash
docker compose up -d
uv run poe test-integration
```

The integration tests create a temporary `test_<id>` database and drop it when the run finishes.

## Run locally in one command

You need Docker Desktop running. From a fresh clone:

```bash
docker compose up --build
```

This starts Postgres (with pgvector), Redis, runs the migrations and loads the sample data once, then starts the API.

- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Liveness: [http://localhost:8000/health](http://localhost:8000/health)
- Readiness (checks the database): [http://localhost:8000/ready](http://localhost:8000/ready)

Stop with `Ctrl+C`, then `docker compose down`. Add `-v` to also delete the database volume.

## Develop and test

| Task | Mac / Linux | Windows |
|---|---|---|
| Run the API with reload | `make dev` | `uv run poe dev` |
| Unit tests (no network) | `make test` | `uv run poe test` |
| Integration tests (needs `docker compose up`) | `make test-integration` | `uv run poe test-integration` |
| Coverage report | `make cov` | `uv run poe cov` |
| Lint and format check | `make lint` | `uv run poe lint` |


## D04 · Docker, Compose and tests


### The image

```text
Image: advisoryatlas:dev
Image ID: 5fa55c4c8840
Disk usage: 300 MB
Content size: 70 MB
Target: under 400 MB — passed.

First build: 9.4 seconds — SUCCESS (20/20 steps).
Second build: 12.9 seconds — SUCCESS (20/20 steps).

Non-root verification:
Command: docker run --rm advisoryatlas:dev id
Output: uid=999(app) gid=999(app) groups=999(app)
Result: Container runs as non-root user.

Docker build cache:
- Copying uv binaries.
- Setting the working directory.
- Creating the non-root app user.
```

### The stack

Command: `docker compose ps -a`

```text
API: Up (healthy)
PostgreSQL: Up (healthy)
Redis: Up (healthy)
Migration: Completed successfully (exit code 0).
```

Migration logs confirmed:
- Created documents and pages.
- Added GIN index on metadata.
- First loader run: 20 inserted.
- Second loader run: 20 unchanged.

### Breaking the database on purpose

```text
With PostgreSQL running:
 /health → status: ok
 /ready  → status: ready, database: True

With PostgreSQL stopped:
 /health → status: ok
 /ready  → status: not_ready, database: False

After PostgreSQL restarted:
 /ready  → status: ready, database: True
```

Result: The API remains healthy when the database stops. Readiness detects database failure and returns to ready after recovery.

A load balancer should stop sending traffic to an instance that is not ready.
Restarting the application does not fix a temporarily unavailable database.

### Tests and coverage

```text
Unit tests:
Command: uv run poe test
Result: 16 passed, 0 failed
Coverage: 83%

Integration tests:
Command: uv run poe test-integration
Result: 7 passed, 0 failed
Coverage: 85%

Combined unit and integration tests:
Result: 23 passed
Total coverage: 96%
Statements: 254
Missing statements: 9
```

### Explanation of uncovered code

1. `deps.py`, lines 37–38: Handles database connection failures and timeouts. Its behaviour was verified by stopping PostgreSQL and checking `/ready`.

2. `middleware.py`, lines 22–24: Handles unexpected errors, logs them and returns HTTP 500 with a request ID. This supports troubleshooting and avoids exposing internal error details.

These are defensive error-handling paths. Their absence from automated coverage does not necessarily indicate a defect.
