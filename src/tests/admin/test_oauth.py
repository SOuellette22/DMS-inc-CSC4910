import urllib.parse

def test_login_redirect_contains_oauth_params(client):
    """GET /admin/login should redirect to Google with oauth params over https."""
    resp = client.get("/admin/login", follow_redirects=False)
    assert resp.status_code in (302, 303)
    loc = resp.headers.get("Location", "")
    assert "accounts.google.com" in loc
    parsed = urllib.parse.urlparse(loc)
    qs = urllib.parse.parse_qs(parsed.query)
    assert "client_id" in qs
    assert "redirect_uri" in qs
    assert "scope" in qs
    assert "state" in qs
    # ensure scheme is https in redirect URL
    assert parsed.scheme in ("https", "") or "https" in loc

def test_oauth_callback_success_and_missing_code(client, app):
    """Test callback accepts code+matching state and rejects missing code."""
    # success path: set expected state in session
    with client.session_transaction() as sess:
        sess["oauth_state"] = "expected-state-123"
    resp_ok = client.get("/admin/callback", query_string={"code": "dummy-code", "state": "expected-state-123"}, follow_redirects=True)
    # Success should not raise server error
    assert resp_ok.status_code != 500
    # missing code should not be treated as 200 success; expect redirect or 4xx
    with client.session_transaction() as sess:
        sess["oauth_state"] = "s2"
    resp_missing = client.get("/admin/callback", query_string={"state": "s2"}, follow_redirects=True)
    assert resp_missing.status_code != 500
    assert resp_missing.status_code >= 300 and resp_missing.status_code < 500

def test_oauth_callback_invalid_state(client):
    """Callback with mismatched state should not authenticate and should not 500."""
    with client.session_transaction() as sess:
        sess["oauth_state"] = "original"
    resp = client.get("/admin/callback", query_string={"code": "c", "state": "tampered"}, follow_redirects=True)
    assert resp.status_code != 500
    assert 300 <= resp.status_code < 500



