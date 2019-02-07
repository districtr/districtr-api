def test_can_list_places(client):
    response = client.get("/places/")
    places = response.get_json()
    assert places == [
        {"id": 1, "name": "Lowell, MA", "description": "A town", "elections": []}
    ]


def test_can_create_new_place_with_elections(
    client, admin_headers, place_record_with_elections
):
    response = client.post(
        "/places/", headers=admin_headers, json=place_record_with_elections
    )
    assert response.status_code == 201
    assert set(response.get_json().keys()) == {"id", "name", "description", "elections"}
