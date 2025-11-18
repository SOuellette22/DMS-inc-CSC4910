SUCCESS_MARKER = b"Rating Submitted Properly"

def post_rate(client, data):
    return client.post("/rate/", data=data, follow_redirects=True)

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

def test_post_missing_fields_is_not_success(client):
    """Omit required fields and assert submission is not considered successful."""
    data = {
        "soil_ph": "6.5",
        # missing many fields intentionally
    }
    resp = post_rate(client, data)
    assert resp.status_code != 500
    assert SUCCESS_MARKER not in resp.data

def test_post_non_numeric_numeric_field_is_handled(client):
    """Non-numeric numeric field (soil_ec) should not crash and should not be a success."""
    data = {
        "soil_ph": "6.5",
        "soil_drainage": "Well Drained",
        "soil_moisture": "Moderate",
        "soil_ec": "not-a-number",
        "flood_frequency": "Rarely",
        "culvert_material": "Concrete",
        "culvert_shape": "Round",
        "culvert_length": "10",
        "culvert_age": "5",
    }
    resp = post_rate(client, data)
    assert resp.status_code != 500
    assert SUCCESS_MARKER not in resp.data

def test_post_negative_and_zero_numbers(client):
    """Negative and zero numeric inputs should be validated (not considered success here)."""
    base = {
        "soil_ph": "6.5",
        "soil_drainage": "Well Drained",
        "soil_moisture": "Moderate",
        "soil_ec": "1.2",
        "flood_frequency": "Rarely",
        "culvert_material": "Concrete",
        "culvert_shape": "Round",
    }
    # negative length
    data_neg = dict(base, culvert_length="-1", culvert_age="5")
    rneg = post_rate(client, data_neg)
    assert rneg.status_code != 500
    assert SUCCESS_MARKER not in rneg.data
    # zero length
    data_zero = dict(base, culvert_length="0", culvert_age="5")
    rzero = post_rate(client, data_zero)
    assert rzero.status_code != 500
    assert SUCCESS_MARKER not in rzero.data

def test_post_extremely_large_numbers_do_not_crash(client):
    """Very large numeric inputs should not cause a server error (may be rejected)."""
    data = {
        "soil_ph": "0.005",
        "soil_drainage": "Well Drained",
        "soil_moisture": "Moderate",
        "soil_ec": "1.234567890123456789",
        "flood_frequency": "Rarely",
        "culvert_material": "Concrete",
        "culvert_shape": "Round",
        "culvert_length": "9999999999999999999999",
        "culvert_age": "99999999",
    }
    resp = post_rate(client, data)
    assert resp.status_code != 500
    # accept either success or a validation rejection, but ensure no crash
    # If your app should accept, change this assert accordingly
    # Here we only ensure it's safe and doesn't return 500
    assert True

def test_methods_not_allowed(client):
    """PUT on the rate route should return 405 or be handled explicitly."""
    resp = client.put("/rate/", data={}, follow_redirects=False)
    assert resp.status_code == 405


# TODO: Add more tests when David is done with the rate page logic