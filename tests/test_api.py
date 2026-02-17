"""Basic API tests - NEEDS MORE TESTS!"""
import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.storage import incidents, tasks, notification_log, escalation_history

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_storage():
    """Clear all storage before each test."""
    incidents.clear()
    tasks.clear()
    notification_log.clear()
    escalation_history.clear()


# =============================================================================
# EXISTING TESTS - These pass
# =============================================================================

def test_create_incident():
    """Test creating an incident."""
    response = client.post("/incidents", json={
        "title": "Test Incident",
        "description": "Test description"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Incident"


def test_list_incidents():
    """Test listing incidents."""
    response = client.get("/incidents")
    assert response.status_code == 200


def test_get_incident_not_found():
    """Test getting non-existent incident."""
    response = client.get("/incidents/nonexistent")
    assert response.status_code == 404


# =============================================================================
# TODO: ADD TESTS FOR NEW FEATURES
# The following features were added but have no tests:
# - Bulk incident creation (/incidents/bulk)
# - CSV export (/incidents/export)
# - Escalation (/incidents/{id}/escalate)
# - Notification (/incidents/{id}/notify)
# =============================================================================

# TODO: Add test for bulk creation
# TODO: Add test for CSV export format
# TODO: Add test for escalation levels
# TODO: Add test for max escalation limit
# TODO: Add test for notification sending

