def test_signin(client):
    resp = client.post("/signin/", json={"email": "person@example.com"})
    assert resp.status_code < 300
