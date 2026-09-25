import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client():
    """A fresh demo-mode API client for every test."""
    with TestClient(app) as test_client:
        yield test_client
