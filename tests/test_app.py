import os
import pytest
from app import app, API_TOKEN

@pytest.fixture
def client():
    app.config.update({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "message" in data

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

def test_info(client):
    resp = client.get("/info")
    assert resp.status_code == 200
    data = resp.get_json()
    for key in ("version", "build_time", "environment"):
        assert key in data

def test_secure_requires_token(client):
    resp = client.get("/secure")
    assert resp.status_code == 401

def test_secure_with_header(client):
    resp = client.get("/secure", headers={"X-API-Token": API_TOKEN})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("secure") is True

def test_secure_with_query_param(client):
    resp = client.get(f"/secure?token={API_TOKEN}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("secure") is True

def test_metrics(client):
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"app_http_requests_total" in resp.data
