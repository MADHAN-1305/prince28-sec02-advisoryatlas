"""The metadata contract for every document in AdvisoryAtlas."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

Short = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=80)]

Values = Annotated[list[Short], Field(default_factory=list, max_length=8)]

Kind = Literal[
    "guideline", "rule", "notice", "list", "report", "faq", "form", "tutorial", "reference", "other"
]

Severity = Literal["critical", "high", "medium", "low", "informational", "unknown"]


class DocMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")

    doc_kind: Kind
    year: int | None = Field(default=None, ge=1950, le=2027)
    language: Literal["en", "ta", "hi", "other"]
    summary: str = Field(min_length=20, max_length=300)
    topics: Annotated[list[Short], Field(min_length=1, max_length=6)]

    # AdvisoryAtlas-specific metadata
    note_id: Values
    severity: Annotated[list[Severity], Field(default_factory=list, max_length=8)]
    vendor: Values
    affected_products: Values
    cve_ids: Values

    @field_validator("topics")
    @classmethod
    def _tidy(cls, value: list[str]) -> list[str]:
        return list(dict.fromkeys(topic.lower() for topic in value))
