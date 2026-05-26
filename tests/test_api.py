import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from main import app
    return TestClient(app)


def test_analyze_valid_code_returns_200(client):
    resp = client.post("/analyze", json={"source": "def foo(arr):\n for x in arr: pass"})
    assert resp.status_code == 200


def test_analyze_returns_list_of_results(client):
    resp = client.post("/analyze", json={"source": "def foo(arr):\n for x in arr: pass"})
    results = resp.json()
    assert isinstance(results, list)
    assert len(results) == 1


def test_analyze_result_fields(client):
    resp = client.post("/analyze", json={"source": "def foo(arr):\n for x in arr: pass"})
    result = resp.json()[0]
    assert result["name"] == "foo"
    assert result["time_complexity"] == "O(n)"
    assert "space_complexity" in result
    assert "explanation" in result


def test_analyze_multiple_functions(client):
    source = "def a(): pass\ndef b(): pass"
    resp = client.post("/analyze", json={"source": source})
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_analyze_no_functions_returns_empty_list(client):
    resp = client.post("/analyze", json={"source": "x = 1"})
    assert resp.status_code == 200
    assert resp.json() == []


def test_analyze_syntax_error_returns_400(client):
    resp = client.post("/analyze", json={"source": "def foo(: pass"})
    assert resp.status_code == 400


def test_analyze_syntax_error_detail_has_message_and_line(client):
    resp = client.post("/analyze", json={"source": "def foo(: pass"})
    detail = resp.json()["detail"]
    assert "message" in detail
    assert "line" in detail


def test_analyze_empty_source_returns_422(client):
    resp = client.post("/analyze", json={"source": ""})
    assert resp.status_code == 422


def test_analyze_whitespace_only_source_returns_422(client):
    resp = client.post("/analyze", json={"source": "   "})
    assert resp.status_code == 422


def test_missing_source_field_returns_422(client):
    resp = client.post("/analyze", json={})
    assert resp.status_code == 422
