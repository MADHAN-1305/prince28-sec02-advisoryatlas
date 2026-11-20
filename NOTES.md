# Engineering notes: AdvisoryAtlas

## D03 · PostgreSQL

### Migrations (upgrade, downgrade, upgrade)

```text
Command: uv run --active alembic downgrade -1

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 30996aea276f -> 6d9bb8be90cd, add gin index on metadata

Command: uv run --active alembic current

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
6d9bb8be90cd

Command: uv run --active alembic upgrade head

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 6d9bb8be90cd -> 30996aea276f, add gin index on metadata

Command: uv run --active alembic history

6d9bb8be90cd -> 30996aea276f (head), add gin index on metadata
<base> -> 6d9bb8be90cd, create documents and pages
```

### The loader is idempotent

```text
Run 1:
records=20 inserted=20 updated=0 unchanged=0

Run 2:
records=20 inserted=0 updated=0 unchanged=20

Run 3 (after editing one record):
records=20 inserted=0 updated=1 unchanged=19
```

### EXPLAIN for ?note_id=CIVN-2023-0280

```text
-- 1) What the planner chooses on its own:
Seq Scan on documents  (cost=0.00..11.00 rows=1 width=36) (actual time=0.783..1.437 rows=1.00 loops=1)
  Filter: (metadata @> '{"note_id": "CIVN-2023-0280"}'::jsonb)
  Rows Removed by Filter: 19
  Buffers: shared read=3 dirtied=3
Planning:
  Buffers: shared hit=143 read=8 dirtied=1
Planning Time: 6.855 ms
Execution Time: 1.473 ms

-- 2) Seq scan switched off, to prove the index can be used:
Bitmap Heap Scan on documents  (cost=12.81..16.82 rows=1 width=36) (actual time=1.886..1.888 rows=1.00 loops=1)
  Recheck Cond: (metadata @> '{"note_id": "CIVN-2023-0280"}'::jsonb)
  Heap Blocks: exact=1
  Buffers: shared hit=2 read=2
  ->  Bitmap Index Scan on ix_documents_metadata_gin  (cost=0.00..12.81 rows=1 width=0) (actual time=1.841..1.841 rows=1.00 loops=1)
        Index Cond: (metadata @> '{"note_id": "CIVN-2023-0280"}'::jsonb)
        Index Searches: 1
        Buffers: shared hit=1 read=2
Planning:
  Buffers: shared hit=1
Planning Time: 0.095 ms
Execution Time: 1.953 ms
```

**Why did the planner choose a Seq Scan on my table?**

The table has only 20 records, so PostgreSQL considers checking all records cheaper than using an index. A sequential scan is reasonable for such a small table.

**When would it switch to the GIN index?**

When the table becomes larger and PostgreSQL estimates that using the index is cheaper than scanning every record.
## D04 · Docker and Testing
### Docker image
First Docker build:
Time: 9.4 seconds
Result: SUCCESS (20/20 steps finished)

Image: advisoryatlas:dev
Image ID: 5fa55c4c8840
Disk usage: 300 MB
Content size: 70 MB
Second Docker build:
Time: 12.9 seconds
Result: SUCCESS (20/20 steps finished)
### Docker Compose status

Command: docker compose ps

API: Up (healthy)
PostgreSQL: Up (healthy)
Redis: Up (healthy)

All 3 containers are running successfully.
### Docker migration logs

Command: docker compose logs migrate

Migrations completed:
- Created documents and pages.
- Added GIN index on metadata.

First loader run:
records=20 inserted=20 updated=0 unchanged=0

Second loader run:
records=20 inserted=0 updated=0 unchanged=20

Result: Migrations and loader completed successfully.
### Database stop and recovery

Command: docker compose stop db

Result: PostgreSQL stopped successfully.

Command: docker compose start db

Result: PostgreSQL started successfully.

Verification: docker compose ps

PostgreSQL: Up (healthy)
API: Up (healthy)
Redis: Up (healthy)

Result: Database recovered successfully without recreating the container.
### Unit test results

Command: uv run poe test

Test folder: tests/unit
Result: 16 passed, 0 failed
Execution time: 0.41 seconds

Status: All unit tests passed.
### Integration test results

Command: uv run poe test-integration

Test folder: tests/integration
Result: 7 passed, 0 failed
Execution time: 4.22 seconds

Status: All integration tests passed.
### Unit test coverage

Command: uv run poe cov

Total coverage: 83%
Statements: 254
Missing statements: 36

Tests: 16 passed, 7 skipped
Execution time: 3.78 seconds

Coverage report: 10 files skipped due to complete coverage.
### Integration test coverage

Command: uv run pytest tests/integration --cov=advisoryatlas --cov-report=term-missing

TEST_DATABASE_URL: Set to local app_test database.

Total coverage: 85%
Statements: 254
Missing statements: 29

Tests: 7 passed, 0 failed
Execution time: 5.33 seconds

Coverage report: 8 files skipped due to complete coverage.
### Explanation of uncovered lines

The integration-only coverage is 85%.
The combined unit and integration coverage is 96%.

The combined report shows 9 uncovered statements.
These represent code paths not executed by the combined test suite.
### Non-root Docker verification

Command: docker run --rm advisoryatlas:dev id

Output:
uid=999(app) gid=999(app) groups=999(app)

Result: Container runs as the non-root app user, not root.

### Docker build cache

Docker reused these layers (marked CACHED in build output):
- Copying uv binaries.
- Setting the working directory.
- Creating the non-root app user.
### API health and readiness verification

With PostgreSQL running:

Command: Invoke-RestMethod http://localhost:8000/health

Output:
status: ok
app: advisoryatlas
env: local

Command: Invoke-RestMethod http://localhost:8000/ready

Output:
status: ready
database: True

With PostgreSQL stopped:

Command: docker compose stop db

Result: PostgreSQL stopped successfully.

Command: Invoke-RestMethod http://localhost:8000/health

Output:
status: ok

Command: Invoke-RestMethod http://localhost:8000/ready

Output:
status: not_ready
database: False

With PostgreSQL restarted:

Command: docker compose start db

Result: PostgreSQL started successfully.

Command: Invoke-RestMethod http://localhost:8000/ready

Output:
status: ready
database: True

Result:
The API remains healthy when the database stops, readiness detects database failure, and readiness returns to ready after database recovery.

### Combined test coverage

Command:
$env:TEST_DATABASE_URL = "postgresql://app:YOUR_PASSWORD@localhost:5433/app_test" # pragma: allowlist secret
uv run --active pytest tests/unit tests/integration --cov=advisoryatlas --cov-report=term-missing

Results:
Total coverage: 96%
Statements: 254
Missing statements: 9
Tests: 23 passed
Execution time: 7.30 seconds

Result: Combined coverage exceeded the expected approximately 92%.

### Examples of uncovered code and their impact

1. API database dependency (deps.py, lines 37-38):
The exception handler returns False when a database connection fails or times out. This prevents a database failure from crashing the health-check process. Its behaviour was verified by stopping PostgreSQL and checking /ready.

2. API middleware (middleware.py, lines 22-24):
The exception handler logs unexpected errors and returns a clean HTTP 500 response with a request ID. This helps protect internal error details and supports troubleshooting.

These uncovered paths are defensive error-handling code. Their absence from automated coverage does not necessarily indicate a defect.

## D05 · Production Deployment, Monitoring and Rollback

### GitHub Actions CI

Repository:
https://github.com/MADHAN-1305/prince28-sec02-advisoryatlas

Workflow: `.github/workflows/ci.yml`

Verification:
- Lint and test: PASSED
- Build image: PASSED
- Unit tests: 25 passed
- Code coverage: 92%

### Production deployment

Platform: Render

Production URL:
https://advisoryatlas.onrender.com

API documentation:
https://advisoryatlas.onrender.com/docs

Health endpoint:
https://advisoryatlas.onrender.com/health

Readiness endpoint:
https://advisoryatlas.onrender.com/ready

Deployment verification:
- Docker image deployed from GitHub Container Registry.
- Production health endpoint returned HTTP 200.
- Readiness endpoint returned HTTP 200.
- Database readiness check: True.
- Documents API returned HTTP 200.
- Production smoke test: PASSED.

Final deployed commit:
`ae29a4db5f3b36ee4158d47467144072e044442a`

### Uptime monitoring

Service: UptimeRobot

Monitor:
- Type: HTTP(S)
- URL: `https://advisoryatlas.onrender.com/health`
- Interval: 5 minutes
- Request method: HEAD
- Monitor status: UP

A public status page was created and linked through a README badge.

Public status page:
https://stats.uptimerobot.com/kZCO9kIPKH

### Health endpoint verification

Production GET request:
`Invoke-RestMethod https://advisoryatlas.onrender.com/health`

Result:
- Status: ok
- App: advisoryatlas
- Environment: production
- Version: `ae29a4db5f3b36ee4158d47467144072e044442a`

GET and HEAD requests both returned HTTP 200.

### Rollback and restoration drill

Procedure:
1. Manually deployed the previous production image using the CD workflow.
2. Verified the previous version through the production smoke test.
3. Triggered another manual CD deployment using the latest main commit.
4. Verified that the latest version was restored.

Rollback version:
`a36fc5771ac6a20d1c90aba521c9e0b4fbad2747`

Restored version:
`ae29a4db5f3b36ee4158d47467144072e044442a`

Final verification:
- `/health`: HTTP 200
- `/ready`: HTTP 200
- Database: True
- `/v1/documents?limit=1`: HTTP 200
- Smoke test: PASSED

Manual PowerShell verification confirmed the restored production version.

Result: Rollback and restoration drill completed successfully.
