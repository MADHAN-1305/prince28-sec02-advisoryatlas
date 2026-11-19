
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
