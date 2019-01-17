def test_can_list_users(client_with_user):
    response = client_with_user.get("/users/")
    assert len(response.get_json()) == 1
