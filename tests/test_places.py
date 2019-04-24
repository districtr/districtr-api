from api.schemas.place import DistrictingProblemSchema, TilesetSchema


def test_can_list_places(client):
    response = client.get("/places/")
    places = response.get_json()
    assert places == [
        {
            "id": 1,
            "name": "Lowell, MA",
            "description": "A town",
            "units": [],
            "districtingProblems": [],
        }
    ]


def test_can_create_new_place_with_elections(
    client, admin_headers, place_record_with_elections
):
    response = client.post(
        "/places/", headers=admin_headers, json=place_record_with_elections
    )
    print(response.get_json())
    assert response.status_code == 201
    assert set(response.get_json().keys()) == {
        "id",
        "name",
        "description",
        "units",
        "districtingProblems",
    }


def test_can_create_new_place_with_tilesets(
    client, admin_headers, place_record_with_tilesets
):
    response = client.post(
        "/places/", headers=admin_headers, json=place_record_with_tilesets
    )
    assert response.status_code == 201
    body = response.get_json()
    assert set(body.keys()) == {
        "id",
        "name",
        "description",
        "units",
        "districtingProblems",
    }
    print(body)
    assert (
        body["units"][0]["tilesets"][0]
        == place_record_with_tilesets["units"][0]["tilesets"][0]
    )


def test_place_record_with_tilesets_is_valid(place_record_with_tilesets):
    schema = TilesetSchema(many=True)
    errors = schema.validate(place_record_with_tilesets["units"][0]["tilesets"])
    assert len(errors) == 0


def test_tileset_schema_can_load_new_tileset(place_record_with_tilesets, app):
    schema = TilesetSchema(many=True)
    with app.app_context():
        tilesets = schema.load(place_record_with_tilesets["units"][0]["tilesets"])
        assert (
            tilesets[0].source_url
            == place_record_with_tilesets["units"][0]["tilesets"][0]["source"]["url"]
        )


def test_can_create_new_place_with_districting_problem(
    place_record_with_districting_problem, admin_headers, client
):
    response = client.post(
        "/places/", headers=admin_headers, json=place_record_with_districting_problem
    )
    assert response.status_code == 201
    assert set(response.get_json().keys()) == {
        "id",
        "name",
        "description",
        "units",
        "districtingProblems",
    }


def test_place_record_with_districting_problems_is_valid(
    place_record_with_districting_problem
):
    schema = DistrictingProblemSchema(many=True)
    errors = schema.validate(
        place_record_with_districting_problem["districtingProblems"]
    )
    assert len(errors) == 0


def test_tilesets_are_required(place_record_with_elections, admin_headers, client):
    del place_record_with_elections["units"][0]["tilesets"]
    response = client.post(
        "/places/", headers=admin_headers, json=place_record_with_elections
    )
    assert response.status_code == 400
