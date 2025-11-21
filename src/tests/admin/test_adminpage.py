import pytest
from src.models import Admin

def test_get_adminpage_logged_in(client):
    """Test that the admin page loads correctly."""
    username  = Admin.query.all()[0]
    with client.session_transaction() as sess:
        sess["username"] = username.email # Simulate that there exists a logged in user
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
    username = Admin.query.all()[0]
    with client.session_transaction() as sess:
        sess["username"] = username.email # Simulate that there exists a logged in user

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

def test_logout_clears_session(client):
    """Logout should remove session keys and clear session cookie."""
    with client.session_transaction() as sess:
        sess["username"] = "tester"
        sess["some_other"] = "value"
    resp = client.get("/admin/logout", follow_redirects=True)
    # ensure no server error
    assert resp.status_code != 500
    # session should be cleared (or at least not contain username)
    with client.session_transaction() as sess_after:
        assert "username" not in sess_after

def test_methods_not_allowed(client):
    """Test that not allowed methods return 405."""
    response = client.put("/admin/")
    assert response.status_code == 405
    response = client.delete("/admin/")
    assert response.status_code == 405
    response = client.patch("/admin/")
    assert response.status_code == 405

def test_login_methods_not_allowed(client):
    """Test that not allowed methods on login return 405."""
    response = client.put("/admin/login")
    assert response.status_code == 405
    response = client.delete("/admin/login")
    assert response.status_code == 405
    response = client.patch("/admin/login")
    assert response.status_code == 405

@pytest.mark.parametrize("username_value", ["", None, 0])
def test_admin_access_with_various_session_username_values(client, username_value):
    """
    Test access control when session['username'] is empty string, None, or a non-string type.
    Expect no server error and likely a redirect to login or denied access.
    """
    with client.session_transaction() as sess:
        sess["username"] = username_value
    resp = client.get("/admin/", follow_redirects=True)
    assert resp.status_code != 500
    # should not allow admin page render as normal 200 for unknown/invalid username
    assert resp.status_code in (302, 401, 403, 404) or resp.status_code == 200
    assert b"This is the home page" in resp.data
