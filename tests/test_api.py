import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.storage import incidents, tasks

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear():
    incidents.clear()
    tasks.clear()

def test_create_incident():
    r = client.post("/incidents", json={
        "title": "Test",
        "description": "Test description"
    })
    assert r.status_code == 200

def test_get_incidents_empty():
    r = client.get("/incidents")
    assert r.status_code == 200
    assert r.json() == []

def test_create_and_get():
    client.post("/incidents", json={"title": "Test", "description": "Desc"})
    r = client.get("/incidents")
    assert len(r.json()) == 1

