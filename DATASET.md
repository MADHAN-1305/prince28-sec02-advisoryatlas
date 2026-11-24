# Dataset: AdvisoryAtlas

Answers 'am I affected?' from CERT-In advisories and vulnerability notes, with the note ID, affected versions and the fix.

- **Start target:** 300 vulnerability notes (last 12 months)
- **Full target:** 1,500+ notes and advisories (3+ years)
- **Collected by:** `scripts/fetch.py` as `examate-student-bot` (https://github.com/MADHAN-1305/prince28-sec02-advisoryatlas): robots.txt respected, at most 4 requests at once, 0.5 s between requests to one site.

## Where the documents come from

- https://www.cert-in.org.in/ (menus: Advisories, Vulnerability Notes)

## Terms I follow

Public government notices. Cite the note ID. Download slowly (1 request every 2 seconds).

- Every answer links to the original document.
- No personal data is collected.

<!-- generated:start -->
## Sources (generated 2026-11-24 04:08 UTC by scripts/dataset_report.py)

| Source | Licence / terms | Files | MB | Pages* | How | Fetched | Example URL |
|---|---|---|---|---|---|---|---|
| cert-in | CERT-In public notice; reproduction requires permission; cite note ID and source | 10 | 0.8 | 15 | http | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIAD-2026-0059&pageid=PUBVLNOTES02 |

**Total:** 10 files, 0.8 MB, 15 pages. Not downloaded: 0 blocked by robots.txt, 0 failed.

*Pages = PDF pages, plus one page per 3,000 characters of text or HTML.

## Files (first 10 of 10)

The complete list, with a sha256 fingerprint of every file, is `data/manifest.jsonl`.

| # | Title / file | Source | Pages | Fetched | URL |
|---|---|---|---|---|---|
| 1 | CIVN-2026-0424 Multiple vulnerabilities in Fortinet Products - Aug 2026 | cert-in | 1 | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIVN-2026-0424&pageid=PUBVLNOTES01 |
| 2 | CIVN-2026-0564 Multiple Vulnerabilities in VMware Products - Nov 2026 | cert-in | 2 | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIVN-2026-0564&pageid=PUBVLNOTES01 |
| 3 | CIVN-2026-0557 Multiple Vulnerabilities in C-DAC e-Sushrut HMIS - Nov 2026 | cert-in | 2 | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIVN-2026-0557&pageid=PUBVLNOTES01 |
| 4 | CIVN-2026-0560 Multiple Vulnerabilities in Citrix NetScaler - Nov 2026 | cert-in | 1 | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIVN-2026-0560&pageid=PUBVLNOTES01 |
| 5 | CIVN-2026-0231 Multiple Vulnerabilities in Microsoft Products - May 2026 | cert-in | 2 | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIVN-2026-0231&pageid=PUBVLNOTES01 |
| 6 | CIVN-2026-0565 Multiple Vulnerabilities in Microsoft Office SharePoint - Nov 2026 | cert-in | 1 | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIVN-2026-0565&pageid=PUBVLNOTES01 |
| 7 | CIAD-2026-0059 Multiple Vulnerabilities in Microsoft Products - Nov 2026 | cert-in | 1 | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIAD-2026-0059&pageid=PUBVLNOTES02 |
| 8 | CIVN-2026-0207 Multiple Vulnerabilities in C-DAC e-Sushrut Solution - Apr 2026 | cert-in | 2 | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIVN-2026-0207&pageid=PUBVLNOTES01 |
| 9 | CIVN-2026-0568 Multiple Vulnerabilities in Oracle Products - Nov 2026 | cert-in | 1 | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIVN-2026-0568&pageid=PUBVLNOTES01 |
| 10 | CIVN-2026-0555 Multiple Vulnerabilities in Fortinet Products - Nov 2026 | cert-in | 2 | 2026-11-23 | https://www.cert-in.org.in/s2cMainServlet?VLCODE=CIVN-2026-0555&pageid=PUBVLNOTES01 |
<!-- generated:end -->

## Known gaps

- Start target: 300 CERT-In vulnerability notes from the last 12 months.
- Full target: 1,500+ notes and advisories covering 3+ years.
- Source registry: 57 URLs (56 vulnerability notes and 1 advisory).
- Actual downloaded files: 11.
- Remaining documents to reach the start target: Not yet verified.
- Automated CERT-In collection and storage permissions remain unconfirmed.
- Some documents may be scanned PDFs with little extractable text.
- More verified documents are required to reach the start target.
