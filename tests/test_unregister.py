"""
Tests for the DELETE /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_unregister_successful(client):
    """Test successful removal of a participant from an activity."""
    response = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert "Removed michael@mergington.edu from Chess Club" in data["message"]


def test_unregister_removes_participant_from_activity(client):
    """Test that unregister actually removes the participant from the activity."""
    # Check initial state - Chess Club has 2 participants
    response = client.get("/activities")
    initial_participants = response.json()["Chess Club"]["participants"]
    assert len(initial_participants) == 2
    assert "michael@mergington.edu" in initial_participants

    # Remove one participant
    client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")

    # Check that they're removed
    response = client.get("/activities")
    final_participants = response.json()["Chess Club"]["participants"]

    assert len(final_participants) == 1
    assert "michael@mergington.edu" not in final_participants
    assert "daniel@mergington.edu" in final_participants  # Other participant still there


def test_unregister_not_signed_up_error(client):
    """Test error when student is not signed up for the activity."""
    response = client.delete("/activities/Basketball%20Team/signup?email=notsignedup@mergington.edu")

    assert response.status_code == 400
    data = response.json()
    assert "Student is not signed up for this activity" in data["detail"]


def test_unregister_activity_not_found_error(client):
    """Test error when activity doesn't exist."""
    response = client.delete("/activities/Nonexistent%20Activity/signup?email=test@mergington.edu")

    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_preserves_other_participants(client):
    """Test that removing one participant doesn't affect others."""
    # Programming Class has 2 participants initially
    response = client.get("/activities")
    initial_participants = response.json()["Programming Class"]["participants"]
    assert len(initial_participants) == 2

    # Remove one participant
    client.delete("/activities/Programming%20Class/signup?email=emma@mergington.edu")

    # Check that only one was removed
    response = client.get("/activities")
    final_participants = response.json()["Programming Class"]["participants"]

    assert len(final_participants) == 1
    assert "emma@mergington.edu" not in final_participants
    assert "sophia@mergington.edu" in final_participants


def test_unregister_can_signup_again(client):
    """Test that after unregistering, a student can sign up again."""
    email = "reusable@mergington.edu"

    # Sign up
    client.post("/activities/Art%20Studio/signup?email=" + email)

    # Verify they're signed up
    response = client.get("/activities")
    assert email in response.json()["Art Studio"]["participants"]

    # Unregister
    client.delete("/activities/Art%20Studio/signup?email=" + email)

    # Verify they're removed
    response = client.get("/activities")
    assert email not in response.json()["Art Studio"]["participants"]

    # Sign up again - should work
    response = client.post("/activities/Art%20Studio/signup?email=" + email)
    assert response.status_code == 200

    # Verify they're back
    response = client.get("/activities")
    assert email in response.json()["Art Studio"]["participants"]


def test_unregister_empty_activity_unchanged(client):
    """Test that trying to unregister from an empty activity gives appropriate error."""
    # Basketball Team starts empty
    response = client.get("/activities")
    assert len(response.json()["Basketball Team"]["participants"]) == 0

    # Try to remove someone who isn't there
    response = client.delete("/activities/Basketball%20Team/signup?email=nobody@mergington.edu")
    assert response.status_code == 400

    # Activity should still be empty
    response = client.get("/activities")
    assert len(response.json()["Basketball Team"]["participants"]) == 0