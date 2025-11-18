def test_get_homepage(client):
    """Test that the homepage loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"This is the home page" in response.data

def test_methods_not_allowed(client):
    """Test that POST requests to the homepage are handled correctly."""
    response = client.post("/")
    assert response.status_code == 405

    response = client.put("/")
    assert response.status_code == 405

    response = client.delete("/")
    assert response.status_code == 405

    response = client.patch("/")
    assert response.status_code == 405
