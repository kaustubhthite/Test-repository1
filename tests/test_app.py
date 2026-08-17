from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_signup_rejects_case_insensitive_duplicate(monkeypatch):
    monkeypatch.setitem(
        activities,
        "Chess Club",
        {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        },
    )

    response = client.post("/activities/Chess Club/signup?email=MICHAEL@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_rejects_unknown_activity():
    response = client.post("/activities/Unknown Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
