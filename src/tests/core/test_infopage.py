def test_get_infopage(client):
    """Test that the info page loads correctly."""
    response = client.get("/info")
    assert response.status_code == 200
    assert b"This is the info page" in response.data

def test_methods_not_allowed(client):
    """Test that POST requests to the info page are handled correctly."""
    response = client.post("/info")
    assert response.status_code == 405

    response = client.put("/info")
    assert response.status_code == 405

    response = client.delete("/info")
    assert response.status_code == 405

    response = client.patch("/info")
    assert response.status_code == 405