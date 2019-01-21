def test_can_list_places(client):
    response = client.get("/places/")
    places = response.get_json()
    assert places == [{"id": 1, "name": "Lowell, MA", "description": "A town"}]
