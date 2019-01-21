def test_can_list_users(client):
    response = client.get("/users/")
    assert len(response.get_json()) >= 1


def test_create_new_user(client, auth_headers):
    response = client.post(
        "/users/",
        json={
            "first": "User",
            "last": "Name",
            "email": "user@example.com",
            "roles": ["user", "admin"],
        },
        headers=auth_headers,
    )
    assert response.status_code == 201


# def test_deleting_a_user_requires_admin_role(client):
# response = client.delete("/users/")
