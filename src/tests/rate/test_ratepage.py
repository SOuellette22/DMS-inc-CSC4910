def test_get_ratepage(client):
    """Test that the rate page loads correctly."""
    response = client.get("/rate/")
    assert response.status_code == 200
    assert b"This is the rate page" in response.data

def test_post_ratepage(client):
    """Test posting data to the rate page."""
    response = client.post(
        "/rate/",
        data={
            "soil_ph": "6.5",
            "soil_drainage": "Well Drained",
            "soil_moisture": "Moderate",
            "soil_ec": "1.2",
            "flood_frequency": "Rarely",
            "culvert_material": "Concrete",
            "culvert_shape": "Round",
            "culvert_length": "10",
            "culvert_age": "5",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    # Checks that the submission was successful
    assert b"Rating Submitted Properly" in response.data

    # Checks that we are redirected to the home page
    assert b"This is the home page" in response.data

# TODO: Add more tests when David is done with the rate page logic