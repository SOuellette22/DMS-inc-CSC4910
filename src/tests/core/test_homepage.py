def test_get_homepage(client):
    """Test that the homepage loads correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"This is the home page" in response.data

def test_post_homepage(client):
    """Test that POST requests to the homepage are handled correctly."""
    response = client.post("/")
    assert response.status_code == 405
