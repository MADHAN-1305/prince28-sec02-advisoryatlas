# Capacity plan: AdvisoryAtlas

Full corpus target: 1,500+ notes and advisories (3+ years)

<!-- generated:start -->
## Measured on my start corpus (2026-11-25 04:17 UTC)

| What | Value |
|---|---|
| Files | 323 |
| Size on disk | 24.8 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 425 |
| Characters of text | 1,274,458 |
| Estimated tokens (characters / 4) | 318,614 |
| Tokens per page | 750 |
| PDFs with almost no text (scanned? OCR is Day 7) | 0 |
| Files not measured (zip, xlsx, unreadable) | 0 |

## Estimate for the full corpus (target: 1,500 files)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 4.6 |
| Tokens | measured tokens x scale | 1.48 M |
| Raw files | measured MB x scale | 115 MB |
| Chunks | tokens / 400 x 1.15 overlap | 4,254 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.26 = Rs 24 |
| Vector storage | chunks x 768 numbers x 4 bytes | 13 MB |
| Text in Postgres | characters x scale x 1.2 | 7 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->

## What I conclude

1. **Is embedding cost a problem?**
   No. The estimated one-time embedding cost for 1,500 documents is $0.26 (approximately Rs 24).

2. **Do vectors and text fit in free Postgres?**
   Estimated vector storage is 13 MB and text storage is 7 MB, totaling 20 MB before indexes and database overhead. This fits within the previously recorded 1 GB allowance, subject to dashboard verification.

3. **Which number am I least sure about?**
   The estimated 1.48 million tokens depends on the characters-per-token assumption and corpus composition. I will measure actual tokenizer output after parsing.

4. **What changes if the corpus grows 10 times?**
   At 15,000 documents, estimated tokens increase to 14.8 million and chunks to approximately 42,540.
   Embedding costs approximately $2.60 (Rs 240), with 130 MB of vectors and 70 MB of text, excluding database overhead.
