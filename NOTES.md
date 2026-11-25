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
## D06 · Collecting the corpus

- **Start target:** 300 CERT-In vulnerability notes (last 12 months).
- **Collected today:** 323 files, 425 pages, 24.8 MB (from DATASET.md).
- **Source registry:** 323 URLs (322 vulnerability notes and 1 advisory).
- **Doors used:** URL list (Door 1).
- **Current status:** 322 vulnerability note URLs registered. All 323 files downloaded and measured; document validation and reuse permission remain pending.

### Licence check

| Source | Licence or terms, in my words | May I show full text in answers? |
|---|---|---|
| CERT-In | Public government cybersecurity notices. Reproduction requires permission and proper attribution to CERT-In. | No, not without permission. Use original summaries, advisory IDs and source links instead. |

### robots.txt

- **Site:** https://www.cert-in.org.in/
- **robots.txt:** Its contents could not be reliably confirmed. The downloader checked the endpoint, but automated collection permission remains unverified.
- **Blocked requests:** The expanded download reported 0 blocked and 0 failed requests out of 323 sources. No restrictions were bypassed.
- **Politeness:** Used a 3-second delay in the interruption and resume test. The expanded download used --delay 2 --max-concurrency 1.

### Kill and resume

- **Run 1:** I pressed Ctrl+C after 7 files.
- **Run 2:** downloaded=3, skipped=7.
- **Run 3:** downloaded=0, skipped=10.
- **Incomplete files:** No `.part` files remained.
- **Manifest:** 10 entries were recorded during the original resume test.

The downloader successfully resumed without fetching completed files again. Temporary `.part` files and the manifest help prevent incomplete downloads from being treated as completed documents.

### Capacity (from docs/CAPACITY.md)

- **Tokens per page, reported:** 750.
- **Full corpus target:** 1,500+ notes and advisories (3+ years).
- **Estimated tokens:** 1.48 million.
- **Estimated chunks:** 4,254.
- **One-time embedding cost:** Approximately ₹24.
- **Estimated vector storage:** 13 MB.
- **Estimated PostgreSQL text storage:** 7 MB.
- **Estimated raw storage:** 115 MB.

### The number that surprised me most

The estimated embedding cost for 1,500 documents is only ₹24, making initial processing affordable.

However, this estimate is based on just 10 files, so a larger representative sample is needed for more reliable capacity planning.

### One thing that went wrong today, and how I fixed it

Git initially refused a commit because `.pre-commit-config.yaml` had unstaged modifications.

I fixed the issue by staging the configuration file and retrying the commit. All pre-commit checks subsequently passed.

### Known limitations

- Only 10 documents were measured against the 300-note start target.
- The source registry contains 57 URLs, but these are not equivalent to 57 downloaded documents.
- Automated collection and storage permissions for CERT-In remain unconfirmed.
- Further verified documents and authorization are needed before expanding collection.
### Day 7 - Parsing quality observations

- Successfully parsed all 10 available HTML advisory files.
- Extracted 21 pages in 11.8 seconds.
- No parsing failures were reported.
- Verified stored documents and pages using Neon SQL Editor.

#### Identified parsing issues

- Document titles are generic, such as "Vulnerability".
- Section headings are empty in the inspected pages.
- Extracted text contains navigation links and website footers.

#### Future improvements

- Extract the actual advisory title.
- Improve section heading detection.
- Remove website navigation and footer content.
- Expand the corpus to at least 20 files for further validation.
### Day 7 - Full corpus parsing and failure analysis

- Successfully parsed 10 out of 10 available files.
- Total extracted pages: 21.
- Full corpus parsing command executed twice.
- 0 failures out of 10 files.
- Verified the parse_failures table using Neon SQL Editor.
- No failed files required repair or retry.
- Manual content comparison is required to assess parsing quality.

## D07 · Parser comparison

<!-- parsers:start -->
| File | Parsers (A / B) | Pages | A found | B found | Time (A / B) | Better, why |
|---|---|---|---|---|---|---|
| s2cmainservlet-2ec087d1.html | trafilatura / strip tags | 1 | 2,251 chars, 0 headings, 0 tables | 5,927 chars, 0 headings, 0 tables | 0.88 s / 0.00 s | Trafilatura preferred: preserves affected versions and removes navigation clutter. |
| s2cmainservlet-2ac4b1a3.html | trafilatura / strip tags | 2 | 3,125 chars, 0 headings, 0 tables | 4,859 chars, 0 headings, 0 tables | 0.11 s / 0.00 s | A preferred provisionally: more compact extraction |
| s2cmainservlet-d862f0df.html | trafilatura / strip tags | 3 | 3,683 chars, 0 headings, 0 tables | 5,828 chars, 0 headings, 0 tables | 0.11 s / 0.00 s | A preferred provisionally: reduced text volume |
| s2cmainservlet-1c3ef068.html | trafilatura / strip tags | 3 | 4,548 chars, 0 headings, 0 tables | 6,022 chars, 0 headings, 0 tables | 0.09 s / 0.00 s | Trafilatura is cleaner but misses the separate affected software list. |
| s2cmainservlet-142979be.html | trafilatura / strip tags | 3 | 3,299 chars, 0 headings, 0 tables | 5,541 chars, 0 headings, 0 tables | 0.08 s / 0.00 s | A preferred provisionally: significant text reduction |
| s2cmainservlet-09e93a67.html | trafilatura / strip tags | 1 | 2,375 chars, 0 headings, 0 tables | 4,223 chars, 0 headings, 0 tables | 0.09 s / 0.00 s | A preferred provisionally: concise extraction |
| s2cmainservlet-4189bf22.html | trafilatura / strip tags | 3 | 4,682 chars, 0 headings, 0 tables | 6,036 chars, 0 headings, 0 tables | 0.15 s / 0.00 s | Trafilatura is cleaner but misses the separate affected system list. |
| s2cmainservlet-37491826.html | trafilatura / strip tags | 1 | 2,522 chars, 0 headings, 0 tables | 4,024 chars, 0 headings, 0 tables | 0.11 s / 0.00 s | A preferred provisionally: shorter extraction |
| s2cmainservlet-d3612498.html | trafilatura / strip tags | 3 | 3,311 chars, 0 headings, 0 tables | 4,994 chars, 0 headings, 0 tables | 0.09 s / 0.00 s | A preferred provisionally: reduced text volume |
| s2cmainservlet-3e2e5828.html | trafilatura / strip tags | 1 | 2,907 chars, 0 headings, 0 tables | 4,610 chars, 0 headings, 0 tables | 0.09 s / 0.00 s | A preferred provisionally: compact extraction |
<!-- parsers:end -->

### Comparison findings

- Compared all 10 available HTML documents.
- Trafilatura extracted fewer characters in all 10 files.
- Plain tag-stripping was faster.
- Neither parser detected structured headings or tables.
- Trafilatura is provisionally preferred for HTML extraction.
- Manual content verification is needed to confirm that important
  advisory information has not been lost.
- PDF comparison was not possible because the current corpus
  contains no PDF documents.


### Manual parser comparison findings

- Compared all 10 available HTML files.
- Manually inspected 3 original HTML documents against
  their corresponding extracted pages in Neon.
- Advisory IDs, titles, dates and severity ratings
  were preserved in the inspected documents.
- Trafilatura reduced navigation and sidebar clutter.
- Separate affected software lists were missing in
  two inspected documents.
- Neither parser detected structured headings or tables.
- Plain tag-stripping was faster.
- Trafilatura is provisionally preferred, but affected
  software extraction requires improvement.
- The remaining seven verdicts are based on automated
  measurements rather than manual content verification.


  ### D07 · Parsing my corpus

- Files in the manifest: 10
- Parsed: 10
- Failed: 0
- Pages in Postgres: 17
- Parsing coverage: 100%

### Failures by reason

0 failures out of 10 files.

### What I saw when I read my parsed pages

- Correct heading path: Multiple Vulnerabilities in
  Microsoft Products, page 2, References.
- Initial issue: CERT-In headings were not extracted
  correctly, and CIAD advisories were not recognized.
- Fix: Improved HTML extraction and added support
  for both CIVN and CIAD formats.
- Existing pages refreshed while preserving document IDs.

### Known gaps

- Only 10 files were collected instead of the target 20.
- The available corpus contains HTML files, not PDFs.
- Real PDF parser performance was not evaluated.

### Verification

- Unit tests: 55 passed.
- Integration tests: 11 passed.
- Ruff lint and formatting: passed.
- Page numbers and heading paths verified in Neon.
