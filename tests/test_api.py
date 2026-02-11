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


def test_get_incidents():
    r = client.get("/incidents")
    assert r.status_code == 200


def test_get_incident():
    create = client.post("/incidents", json={"title": "Test", "description": "Desc"})
    inc_id = create.json()["id"]
    r = client.get(f"/incidents/{inc_id}")
    assert r.status_code == 200


def test_create_task():
    inc = client.post("/incidents", json={"title": "Test", "description": "Desc"}).json()
    r = client.post(f"/incidents/{inc['id']}/tasks", json={"title": "Task 1"})
    assert r.status_code == 200


def test_stats():
    r = client.get("/stats")
    assert r.status_code == 200

