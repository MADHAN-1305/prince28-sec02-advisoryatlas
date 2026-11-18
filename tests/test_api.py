def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_ready_when_database_up(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["checks"]["database"] is True


def test_ready_when_database_down(client, db_state):
    db_state["up"] = False
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json()["checks"]["database"] is False


def test_list_documents(client):
    response = client.get("/v1/documents")
    assert response.status_code == 200
    assert response.json()["total"] == 3


def test_limit(client):
    response = client.get("/v1/documents?limit=1")
    assert len(response.json()["items"]) == 1


def test_offset(client):
    response = client.get("/v1/documents?offset=1")
    assert response.json()["items"][0]["id"] == "002"


def test_search(client):
    response = client.get("/v1/documents?q=Alpha")
    assert response.json()["total"] == 1


def test_search_case_insensitive(client):
    response = client.get("/v1/documents?q=alpha")
    assert response.json()["total"] == 1


def test_filter_kind(client):
    response = client.get("/v1/documents?kind=circular")
    assert response.json()["total"] == 2


def test_filter_year(client):
    response = client.get("/v1/documents?year=2023")
    assert response.json()["total"] == 1


def test_combined_filters(client):
    response = client.get("/v1/documents?kind=circular&year=2024")
    assert response.json()["total"] == 1


def test_no_matching_documents(client):
    response = client.get("/v1/documents?q=unknown")
    assert response.json()["total"] == 0


def test_invalid_filter(client):
    response = client.get("/v1/documents?Bad-Name=1")
    assert response.status_code == 400


def test_list_echoes_filters(client):
    response = client.get("/v1/documents?kind=circular")
    assert response.json()["filters"]["kind"] == "circular"


def test_get_existing_document(client):
    response = client.get("/v1/documents/001")
    assert response.status_code == 200
    assert response.json()["id"] == "001"


def test_get_missing_document(client):
    response = client.get("/v1/documents/999")
    assert response.status_code == 404
