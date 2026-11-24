# AdvisoryAtlas — Day 6, Milestone 4 status

Prepared: 24 November 2026

## Scope

Target: 300 distinct CERT-In vulnerability notes issued within the previous 12 months (24 November 2025 to 24 November 2026). A file in the CSV is a source *link*, not proof it has been downloaded.

## Verified progress

- 57 unique source URL entries in `AdvisoryAtlas_sources_57.csv`, including **56 vulnerability-note IDs** (`CIVN`) and **one advisory ID** (`CIAD`).
- The earlier 44-entry registry has been preserved and 13 additional individual official CERT-In note URLs identified in current public search results were added.
- Duplicate URLs: 0; missing terms/`licence` fields: 0.
- **Remaining note registry entries to reach 300:** 244; subject to checking each note's date and link.
- **Downloaded file count: unknown** because the local repository and `data/manifest.jsonl` were not accessible here.
- **Not complete:** 300 downloaded notes has not been established.

## Rights and access

CERT-In's copyright policy says reproduction requires prior permission. The site's `robots.txt` and automated-storage authorization could not be conclusively verified. Keep the live downloader disabled for CERT-In until collection and storage have been authorized. Delay at least 2 seconds per request if authorized; never exceed 4 simultaneous downloads, and prefer 1 for CERT-In.

## What applies from the lab

- Door 1: applicable for an approved, verified CSV of CERT-In note URLs.
- Door 2: not applicable to CERT-In notes (they do not live in a GitHub repository).
- Door 3: only if CERT-In publishes a reachable sitemap covering these document URLs and permits automated access; not confirmed.
- Door 4: permissible only when the copyright/terms authorize the personal downloads and retention. A blocked bot does not imply manual reproduction is approved.

## Reproducible checks in the local project

```powershell
uv run python -c "from pathlib import Path;from advisoryatlas.ingest.fetch import read_sources;s=read_sources(Path('data/sources.csv'));print('Unique URLs:',len(s),'CIVN notes:',sum('CIVN-' in x.url for x in s))"
```

After authorized collections, inspect manifest statuses; **do not count lines in the JSONL as distinct downloaded documents** because the log is append-only:

```powershell
uv run python -c "import json;from pathlib import Path;p=Path('data/manifest.jsonl');r={x['url']:x for x in (json.loads(line) for line in p.read_text(encoding='utf-8').splitlines())};print('Distinct successful files:',sum(x['status']=='downloaded' and Path(x['path']).is_file() for x in r.values()))"
```

## Note for trainer

The start target is not met. The source URL registry contains 56 registered CIVN note IDs, but downloading and reusing CERT-In material needs rights clarification. The 2-second delay is a politeness constraint, not permission. Request an approved source, authorisation, or a change of scope rather than using an unapproved crawler.

## Source policies

- https://www.cert-in.org.in/s2cMainServlet?pageid=COPYRIGHTPOCY
- https://www.cert-in.org.in/s2cMainServlet?pageid=TERMSOFUSE
- https://www.cert-in.org.in/s2cMainServlet?pageid=VLNLIST02&year=2026
