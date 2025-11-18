def test_get_adminpage_logged_in(client):
    """Test that the admin page loads correctly."""
    with client.session_transaction() as sess:
        sess["username"] = True # Simulate that there exists a logged in user
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b"This is the admin page" in response.data

def test_get_adminpage_not_logged_in(client):
    """Test that the admin page redirects to login when not logged in."""
    response = client.get("/admin/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin/login")

def test_login_redirect(client):
    """Test that the login route redirects to Google OAuth."""
    response = client.get("/admin/login")
    assert response.status_code == 302
    assert "accounts.google.com" in response.headers["Location"]

def test_login_already_logged_in(client):
    """Test that accessing login when already logged in redirects to admin index."""
    with client.session_transaction() as sess:
        sess["username"] = True # Simulate that there exists a logged in user
    response = client.get("/admin/login")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin/")

def test_log_out(client):
    """Test that the logout route clears the session and redirects to home."""
    with client.session_transaction() as sess:
        sess["username"] = True # Simulate that there exists a logged in user

    # Checks to make sure the user is logged in
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b"This is the admin page" in response.data

    # Logs out the user
    response = client.get("/admin/logout")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

def test_log_out_not_logged_in(client):
    """Test that logging out when not logged in still redirects to home."""
    response = client.get("/admin/logout")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
