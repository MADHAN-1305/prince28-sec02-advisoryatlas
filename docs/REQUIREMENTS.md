
# AdvisoryAtlas – Project Requirements

## 1. Functional Requirements

### FR-01: Vulnerability Data Collection
The system shall collect CERT-In vulnerability notes and advisories published within the last 3+ years.

### FR-02: Product Registration
The system shall allow an IT administrator to register products and their installed versions.

### FR-03: Version Range Matching
The system shall compare registered product versions against parsed vulnerability version ranges and identify whether a product is affected.

### FR-04: Vulnerability Results
The system shall display the CERT-In note ID, affected product versions and recommended fix for each matching vulnerability.

### FR-05: My-Stack Checker
The system shall display an Affected, Not affected or Check manually status for each registered product based on available vulnerability information.

## 2. Non-Functional Requirements

### NFR-01: Matching Accuracy
The system shall achieve at least 90% affected/not-affected correctness across 40 product-version test cases.

### NFR-02: Data Collection Rate
The system shall wait at least 2 seconds between requests to the CERT-In website.

### NFR-03: API Documentation
The application shall expose interactive API documentation through the FastAPI `/docs` endpoint.

### NFR-04: Code Quality
The project shall use Ruff for Python linting and pytest for automated testing.

### NFR-05: Version Reproducibility
The project shall use uv and maintain a `uv.lock` file to record dependency versions for reproducible installations.
