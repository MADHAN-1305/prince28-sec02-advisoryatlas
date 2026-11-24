# Capacity plan: AdvisoryAtlas

Full corpus target: 1,500+ notes and advisories (3+ years)

<!-- generated:start -->
## Measured on my start corpus (2026-11-24 04:08 UTC)

| What | Value |
|---|---|
| Files | 10 |
| Size on disk | 0.8 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 15 |
| Characters of text | 46,351 |
| Estimated tokens (characters / 4) | 11,588 |
| Tokens per page | 750 |
| PDFs with almost no text (scanned? OCR is Day 7) | 0 |
| Files not measured (zip, xlsx, unreadable) | 0 |

## Estimate for the full corpus (target: 1,500 files)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 150.0 |
| Tokens | measured tokens x scale | 1.74 M |
| Raw files | measured MB x scale | 116 MB |
| Chunks | tokens / 400 x 1.15 overlap | 4,997 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.30 = Rs 28 |
| Vector storage | chunks x 768 numbers x 4 bytes | 15 MB |
| Text in Postgres | characters x scale x 1.2 | 8 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->

## What I conclude

1. **Is embedding cost a problem?**
   No. Embedding the full corpus of 1,500 documents is estimated to cost only $0.30 (approximately ₹28), which is affordable for this project.

2. **Do vectors and text fit in free Postgres?**
   Yes, based on the estimate. Vectors require 15 MB and text requires 8 MB, totaling approximately 23 MB. Neon's Free plan provides 1 GB per project, so the estimated data fits comfortably, excluding indexes, existing data and other overhead.

3. **Which number am I least sure about?**
   The estimated token count of 1.74 million is the most uncertain because it is extrapolated from only 10 files. I will measure a larger, representative sample of at least 100 documents to improve accuracy.

4. **What changes if the corpus grows 10 times?**
   At 15,000 documents, estimated tokens increase to 17.4 million, chunks to approximately 49,970, and one-time embedding cost to $3 (approximately ₹285).
   Vector storage increases to 150 MB and text storage to 80 MB, totaling approximately 230 MB, excluding database overhead.
