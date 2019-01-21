from api.schemas import PlanSchema


def test_create_plan(client, plan_record, auth_headers):
    response = client.post("/plans/", json=plan_record, headers=auth_headers)
    assert response.status_code == 201


def test_created_plan_shows_up_in_list(client, auth_headers, plan_record):
    number_of_plans = len(client.get("/plans/").get_json())
    client.post("/plans/", json=plan_record, headers=auth_headers)
    response = client.get("/plans/")

    assert len(response.get_json()) == number_of_plans + 1


def test_creating_single_plan_returns_its_id(client, auth_headers, plan_record):
    response = client.post("/plans/", json=plan_record, headers=auth_headers)
    assert "id" in response.get_json()


def test_creating_a_plan_requires_authentication(client, plan_record):
    response = client.post("/plans/", json=plan_record)
    assert response.status_code == 403


def test_can_get_single_plan_by_id(client, plan_record):
    print(plan_record)
    expected = {
        "id": 1,
        "name": plan_record["name"],
        "mapping": plan_record["mapping"],
        "user": {
            "id": 1,
            "first": "Max",
            "last": "Hully",
            "email": "max.hully@gmail.com",
        },
    }
    response = client.get("/plans/1")
    assert response.get_json() == expected


def test_single_plan_records_have_users(client):
    response = client.get("/plans/1")
    assert "user" in response.get_json()


def test_plan_record_is_loadable(plan_record):
    schema = PlanSchema()
    schema.load(plan_record)
