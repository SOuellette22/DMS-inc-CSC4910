def test_get_whypage(client):
    """Test that the why page loads correctly."""
    response = client.get("/why")
    assert response.status_code == 200
    assert b"This is the why page" in response.data

def test_post_whypage(client):
    """Test that POST requests to the why page are handled correctly."""
    response = client.post("/why")
    assert response.status_code == 405