def test_errors_return_json_response(client):
    resp = client.get("/users/not_a_user/")
    result = resp.get_json()
    assert result == {"status": 404, "message": "Resource not found."}
