def test_validation_error_is_caught(client):
    resp = client.post("/register/", json={"wrong_schema": "so wrong"})
    assert resp.status_code != 500
