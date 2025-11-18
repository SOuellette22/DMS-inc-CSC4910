def test_get_infopage(client):
    """Test that the info page loads correctly."""
    response = client.get("/info")
    assert response.status_code == 200
    assert b"This is the info page" in response.data

def test_post_infopage(client):
    """Test that POST requests to the info page are handled correctly."""
    response = client.post("/info")
    assert response.status_code == 405