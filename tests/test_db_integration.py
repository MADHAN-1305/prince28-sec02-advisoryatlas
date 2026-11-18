import os

import pytest
from fastapi.testclient import TestClient

from advisoryatlas.api.main import create_app
from advisoryatlas.config import Settings

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

pytestmark = pytest.mark.skipif(
    not TEST_DATABASE_URL,
    reason="TEST_DATABASE_URL is not configured",
)


@pytest.fixture
def integration_client():
    settings = Settings(
        app_env="test",
        database_url=TEST_DATABASE_URL,
        _env_file=None,
    )

    app = create_app(settings)

    with TestClient(app) as client:
        yield client


def test_database_ready(integration_client):
    response = integration_client.get("/ready")
    assert response.status_code == 200
    assert response.json()["checks"]["database"] is True


def test_list_documents_from_database(integration_client):
    response = integration_client.get("/v1/documents?limit=3")
    assert response.status_code == 200
    assert "items" in response.json()
    assert len(response.json()["items"]) <= 3


def test_document_filters_from_database(integration_client):
    response = integration_client.get("/v1/documents?limit=3")
    assert response.status_code == 200

    items = response.json()["items"]

    if items and items[0].get("note_id"):
        note_id = items[0]["note_id"]
        filtered = integration_client.get(
            "/v1/documents",
            params={"note_id": note_id},
        )
        assert filtered.status_code == 200
        assert all(item["note_id"] == note_id for item in filtered.json()["items"])
