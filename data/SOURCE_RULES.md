# AdvisoryAtlas — CERT-In Sources and Reuse Checks

Checked: 2026-11-23

## Source

- Publisher: Indian Computer Emergency Response Team (CERT-In), Ministry of Electronics and Information Technology, Government of India.
- Source website: https://www.cert-in.org.in/
- Direct vulnerability-note/advisory list: https://www.cert-in.org.in/s2cMainServlet?pageid=VLNLIST02

## Official rules

- robots.txt: https://www.cert-in.org.in/robots.txt — attempt to retrieve was unsuccessful. The site-specific robot directives **could not be verified**; do not equate this with unrestricted crawling permission.
- Copyright Policy: https://www.cert-in.org.in/s2cMainServlet?pageid=COPYRIGHTPOCY — reproduction is allowed free of charge only after obtaining permission by email; attribution required when publishing/issuing content, and third-party material requires separate authorization.
- Terms of Use: https://www.cert-in.org.in/s2cMainServlet?pageid=TERMSOFUSE — informational purpose, disclaimers, external-link terms and jurisdiction; it does not explicitly grant bulk automated collection rights.
- Copyright contact: webmaster@cert-in.org.in (from CERT-In copyright policy).

## Decision record

| Question | Finding |
| --- | --- |
| May a program download advisories automatically? | Not established. Do not assume yes from public access or a missing/unavailable robots.txt. |
| May we store downloaded copies? | Not explicitly authorized by reviewed pages. Clarification/permission may be needed. |
| May we show them in answers? | Provide original brief summaries, note IDs, and direct official URLs. Reproducing original material requires permission and attribution. |
| What delay should a permitted fetcher use? | At least 2 seconds between requests (`--delay 2`), as required by the project card; delay alone is not authorization. |

## Selection rationale

The ten entries in `sources.csv` are directly linked public CERT-In document pages from 2026, selected for hospital IT exposure checking across Windows, Fortinet products, C-DAC e-Sushrut HMIS, VMware, Citrix, Oracle and SharePoint. They give a foundation for testing product/version identification, note IDs, remediation references, and multiple vendor advisories. They are source *metadata* only: the files are not downloaded or mirrored here.

## CSV 'licence' convention

Each row's `licence` value is a plain-language summary of applicable conditions, **not** an open copyright licence, a grant of permission, or proof that the downloader may fetch the URL. If the downloader only checks for a nonempty value, that check is not a legal permission check. Keep automated downloading paused until permitted.
