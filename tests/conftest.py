"""
Shared test fixtures and configuration for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src import app


@pytest.fixture
def client():
    """Test client for making requests to the FastAPI app."""
    return TestClient(app.app)


@pytest.fixture
def test_activities():
    """Fresh copy of activities data for each test to ensure isolation."""
    return deepcopy(app.activities)


@pytest.fixture(autouse=True)
def reset_activities(test_activities):
    """Reset the global activities dict before each test."""
    original_activities = app.activities
    app.activities = test_activities
    yield
    # Reset after test completes
    app.activities = original_activities