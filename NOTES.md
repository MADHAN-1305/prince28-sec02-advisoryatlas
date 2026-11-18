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
