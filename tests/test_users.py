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


def test_create_new_user_requires_admin_role(client):
    response = client.post(
        "/users/",
        json={
            "first": "User",
            "last": "Name",
            "email": "user@example.com",
            "roles": ["user", "admin"],
        },
    )
    assert response.status_code == 403


def test_deleting_a_user_requires_admin_role(client, auth_headers):
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
    user_id = response.get_json()["id"]

    # Try to delete without admin auth headers
    assert client.delete("/users/{}".format(user_id)).status_code == 403

    # Can delete with admin auth headers
    deletion_response = client.delete("/users/{}".format(user_id), headers=auth_headers)
    assert deletion_response.status_code == 204
