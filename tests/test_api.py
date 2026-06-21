from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


@patch('backend.main.GoogleSearch')
def test_search_endpoint_success(mock_google_search):
    # Set up the mock to return a specific dictionary
    mock_instance = MagicMock()
    mock_instance.get_dict.return_value = {
        "organic_results": [
            {"title": "Test Result", "link": "https://test.com", "snippet": "Test snippet"}
        ]
    }

    mock_google_search.return_value = mock_instance

    # Send a POST request to the endpoint
    response = client.post("/api/search", json={"query": "test"})

    # Check that the response status is 200
    assert response.status_code == 200

    # Check that the response content matches our mock data
    data = response.json()
    assert "results" in data
    assert data["results"][0]["title"] == "Test Result"


@patch('backend.main.GoogleSearch')
def test_search_endpoint_no_results(mock_google_search):
    # Setup mock to return an empty organic_results list
    mock_instance = MagicMock()
    mock_instance.get_dict.return_value = {"organic_results": []}
    mock_google_search.return_value = mock_instance

    # Send request
    response = client.post("/api/search", json={"query": "empty"})

    # Should return 404 as handled in main.py
    assert response.status_code == 404


def test_search_endpoint_validation_error():
    # Sending invalid data (missing 'query' field)
    response = client.post("/api/search", json={"wrong_key": "data"})
    # Expect 422 error for Pydantic validation failure
    assert response.status_code == 422


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running perfectly!"}
