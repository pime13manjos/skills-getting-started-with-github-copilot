"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()

    # Should return all 9 activities
    assert len(data) == 9

    # Check that all expected activities are present
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Swimming Club", "Art Studio", "Drama Club", "Debate Team", "Science Club"
    ]

    for activity in expected_activities:
        assert activity in data


def test_get_activities_structure(client):
    """Test that each activity has the correct structure."""
    response = client.get("/activities")
    data = response.json()

    # Check structure for one activity
    chess_club = data["Chess Club"]
    required_fields = ["description", "schedule", "max_participants", "participants"]

    for field in required_fields:
        assert field in chess_club

    # Verify data types
    assert isinstance(chess_club["description"], str)
    assert isinstance(chess_club["schedule"], str)
    assert isinstance(chess_club["max_participants"], int)
    assert isinstance(chess_club["participants"], list)


def test_get_activities_participants_data(client):
    """Test that participants data is accurate."""
    response = client.get("/activities")
    data = response.json()

    # Chess Club should have 2 participants
    chess_club = data["Chess Club"]
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]

    # Programming Class should have 2 participants
    programming = data["Programming Class"]
    assert len(programming["participants"]) == 2
    assert "emma@mergington.edu" in programming["participants"]
    assert "sophia@mergington.edu" in programming["participants"]

    # Gym Class should have 2 participants
    gym = data["Gym Class"]
    assert len(gym["participants"]) == 2
    assert "john@mergington.edu" in gym["participants"]
    assert "olivia@mergington.edu" in gym["participants"]

    # Empty activities should have empty participants list
    basketball = data["Basketball Team"]
    assert len(basketball["participants"]) == 0
    assert basketball["participants"] == []


def test_get_activities_max_participants(client):
    """Test that max_participants values are correct."""
    response = client.get("/activities")
    data = response.json()

    # Verify specific max_participants values
    assert data["Chess Club"]["max_participants"] == 12
    assert data["Programming Class"]["max_participants"] == 20
    assert data["Gym Class"]["max_participants"] == 30
    assert data["Basketball Team"]["max_participants"] == 15
    assert data["Swimming Club"]["max_participants"] == 20
    assert data["Art Studio"]["max_participants"] == 15
    assert data["Drama Club"]["max_participants"] == 25
    assert data["Debate Team"]["max_participants"] == 16
    assert data["Science Club"]["max_participants"] == 20