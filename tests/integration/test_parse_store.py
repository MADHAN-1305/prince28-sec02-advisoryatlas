"""Parsed documents and parse failures, written to a real Postgres."""

import pytest
from sqlalchemy import func, select

from advisoryatlas.config import Settings
from advisoryatlas.db.models import Document, Page, ParseFailure
from advisoryatlas.db.session import make_engine, make_sessionmaker
from advisoryatlas.ingest.parse import ParsedDoc, ParsedPage, ParseError
from advisoryatlas.ingest.store import (
    document_id,
    parsed_ids,
    refresh_document,
    save_document,
    save_failure,
)

RECORD = {
    "url": "https://example.org/fever.pdf",
    "source": "example",
    "licence": "CC BY 4.0",
    "title": "",
    "path": "data/raw/example/fever-1a2b3c4d.pdf",
    "sha256": "ab" * 32,
}
PARSED = ParsedDoc(
    parser="pymupdf",
    kind="pdf",
    title="Fever Guidelines",
    pages=[
        ParsedPage(1, "# Fever Guidelines\n\n## Dengue\n\nRest and fluids.", []),
        ParsedPage(2, "Review after two days.", ["Fever Guidelines", "Dengue"]),
    ],
)


@pytest.fixture
async def session(database_url):
    engine = make_engine(Settings(app_env="ci", database_url=database_url, _env_file=None))
    async with make_sessionmaker(engine)() as db:
        await db.execute(Document.__table__.delete())
        await db.execute(ParseFailure.__table__.delete())
        await db.commit()
        yield db
    await engine.dispose()


async def test_a_parsed_document_is_saved_with_pages_and_heading_paths(session):
    await save_document(session, RECORD, PARSED)
    doc = await session.scalar(select(Document))
    assert doc.external_id == document_id(RECORD["sha256"]) and doc.doc_type == "pdf"
    assert doc.title == "Fever Guidelines" and doc.metadata_["pages"] == 2
    pages = (await session.scalars(select(Page).order_by(Page.page_no))).all()
    assert [p.page_no for p in pages] == [1, 2]
    assert pages[1].headings == ["Fever Guidelines", "Dengue"]
    assert await parsed_ids(session) == {doc.external_id}


async def test_a_failure_is_one_row_however_often_it_fails(session):
    error = ParseError("no_text_layer", "0 characters on 4 pages: needs OCR")
    await save_failure(session, RECORD, error)
    await save_failure(session, RECORD, error)
    row = await session.scalar(select(ParseFailure))
    await session.refresh(row)
    assert await session.scalar(select(func.count()).select_from(ParseFailure)) == 1
    assert row.reason == "no_text_layer" and row.attempts == 2


async def test_a_later_success_clears_the_failure(session):
    await save_failure(session, RECORD, ParseError("corrupt", "bad xref"))
    await save_document(session, RECORD, PARSED)
    assert await session.scalar(select(func.count()).select_from(ParseFailure)) == 0
    assert await session.scalar(select(func.count()).select_from(Page)) == 2


async def test_refresh_preserves_document_and_page_ids(session):
    await save_document(session, RECORD, PARSED)

    original = await session.scalar(select(Document))
    original_id = original.id

    original_page = await session.scalar(select(Page).where(Page.page_no == 1))
    original_page_id = original_page.id

    updated = ParsedDoc(
        parser="pymupdf",
        kind="pdf",
        title="Updated Fever Guidelines",
        pages=[
            ParsedPage(
                1,
                "# Updated Fever Guidelines\n\nUpdated content.",
                ["Updated Fever Guidelines"],
            )
        ],
    )

    await refresh_document(session, RECORD, updated)
    await refresh_document(session, RECORD, updated)

    doc = await session.scalar(select(Document))
    pages = (await session.scalars(select(Page).order_by(Page.page_no))).all()

    assert doc.id == original_id
    assert doc.title == "Updated Fever Guidelines"
    assert doc.metadata_["pages"] == 1
    assert len(pages) == 1
    assert pages[0].id == original_page_id
    assert pages[0].headings == ["Updated Fever Guidelines"]
    assert "Updated content." in pages[0].text

    assert await session.scalar(select(func.count()).select_from(Document)) == 1
