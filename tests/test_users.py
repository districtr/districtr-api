def test_can_list_users(client):
    response = client.get("/users/")
    assert len(response.get_json()) >= 1
