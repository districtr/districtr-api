from api.schemas.place import TilesetSchema


def test_can_list_places(client):
    response = client.get("/places/")
    places = response.get_json()
    assert places == [
        {
            "id": 1,
            "name": "Lowell, MA",
            "description": "A town",
            "elections": [],
            "tilesets": [],
        }
    ]


def test_can_create_new_place_with_elections(
    client, admin_headers, place_record_with_elections
):
    response = client.post(
        "/places/", headers=admin_headers, json=place_record_with_elections
    )
    assert response.status_code == 201
    assert set(response.get_json().keys()) == {
        "id",
        "name",
        "description",
        "elections",
        "tilesets",
    }


def test_can_create_new_place_with_tilesets(
    client, admin_headers, place_record_with_tilesets
):
    response = client.post(
        "/places/", headers=admin_headers, json=place_record_with_tilesets
    )
    assert response.status_code == 201
    body = response.get_json()
    assert set(body.keys()) == {"id", "name", "description", "tilesets", "elections"}
    assert body["tilesets"][0] == place_record_with_tilesets["tilesets"][0]


def test_place_record_with_tilesets_is_valid(place_record_with_tilesets):
    schema = TilesetSchema(many=True)
    errors = schema.validate(place_record_with_tilesets["tilesets"])
    assert len(errors) == 0


def test_tileset_schema_can_load_new_tileset(place_record_with_tilesets, app):
    schema = TilesetSchema(many=True)
    with app.app_context():
        tilesets = schema.load(place_record_with_tilesets["tilesets"])
        assert (
            tilesets[0].source_url
            == place_record_with_tilesets["tilesets"][0]["source"]["url"]
        )
