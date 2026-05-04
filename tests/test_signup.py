"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_successful(client):
    """Test successful signup for an activity."""
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")

    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert "Signed up test@mergington.edu for Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity."""
    # Sign up a new participant
    client.post("/activities/Basketball%20Team/signup?email=newstudent@mergington.edu")

    # Check that they're now in the activity
    response = client.get("/activities")
    data = response.json()

    basketball = data["Basketball Team"]
    assert "newstudent@mergington.edu" in basketball["participants"]
    assert len(basketball["participants"]) == 1


def test_signup_already_registered_error(client):
    """Test error when student is already signed up for the activity."""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    # Second signup with same email should fail
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up for this activity" in data["detail"]


def test_signup_activity_not_found_error(client):
    """Test error when activity doesn't exist."""
    response = client.post("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")

    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_preserves_existing_participants(client):
    """Test that signing up a new participant doesn't remove existing ones."""
    # Chess Club already has 2 participants
    response = client.get("/activities")
    initial_chess_participants = response.json()["Chess Club"]["participants"]
    assert len(initial_chess_participants) == 2

    # Add a new participant
    client.post("/activities/Chess%20Club/signup?email=newguy@mergington.edu")

    # Check that all participants are still there
    response = client.get("/activities")
    final_chess_participants = response.json()["Chess Club"]["participants"]

    assert len(final_chess_participants) == 3
    assert "michael@mergington.edu" in final_chess_participants
    assert "daniel@mergington.edu" in final_chess_participants
    assert "newguy@mergington.edu" in final_chess_participants


def test_signup_multiple_activities(client):
    """Test that a student can sign up for multiple different activities."""
    email = "multiactivity@mergington.edu"

    # Sign up for two different activities
    client.post("/activities/Basketball%20Team/signup?email=" + email)
    client.post("/activities/Swimming%20Club/signup?email=" + email)

    # Check both activities
    response = client.get("/activities")
    data = response.json()

    assert email in data["Basketball Team"]["participants"]
    assert email in data["Swimming Club"]["participants"]


def test_signup_special_characters_in_activity_name(client):
    """Test signup with activity names containing special characters."""
    # Test activity with spaces (already tested above)
    # Test activity with other special characters if they existed
    # For now, just verify existing activities work
    response = client.post("/activities/Programming%20Class/signup?email=special@mergington.edu")
    assert response.status_code == 200