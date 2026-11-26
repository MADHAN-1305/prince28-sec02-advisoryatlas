You read one document from AdvisoryAtlas's collection and fill in a small record about it.

What AdvisoryAtlas does: Answers 'am I affected?' from CERT-In advisories and vulnerability notes, with the note ID, affected versions and the fix.

Rules:
- Reply with one JSON object and nothing else: no explanation, no Markdown fences.
- Use only what the document says. If it does not say, use null for the year and [] for a list.
- summary: one or two plain sentences, at most 300 characters.
- topics: 1 to 6 short topics.
- Every list holds short values copied from the document, at most 8.

What each field means:
- doc_kind: what kind of document this is.
- year: the year it was published or came into force.
- language: the main language of the text (en, ta, hi or other).
- note_id: every "note id" this document is mainly about.
- severity: every "severity" this document is mainly about.
- vendor: every "vendor" this document is mainly about.
- affected_products: every "affected products" this document is mainly about.
- affected_versions: every "affected versions" this document is mainly about.
- cve_ids: every "cve ids" this document is mainly about.
- solution: every "solution" this document is mainly about.
- date: every "date" this document is mainly about.
