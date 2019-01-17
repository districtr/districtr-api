import pytest

from api.schemas import PlanSchema


@pytest.fixture
def client_with_plan(client_with_user, plan_record):
    client_with_user.post("/plans/", json=plan_record)
    return client_with_user


@pytest.fixture
def plan_record():
    return {"id": 1, "name": "My plan", "mapping": {"1": 0}, "user_id": 1}


def test_create_plan(client, plan_record):
    response = client.post("/plans/", json=plan_record)
    assert response.status_code == 201


def test_created_plan_shows_up_in_list(client, plan_record):
    client.post("/plans/", json=plan_record)
    response = client.get("/plans/")
    assert len(response.get_json()) == 1


def test_creating_single_plan_returns_its_id(client, plan_record):
    response = client.post("/plans/", json=plan_record)
    assert "id" in response.get_json()


def test_can_get_single_plan_by_id(client_with_plan, plan_record):
    expected = {
        "id": plan_record["id"],
        "name": plan_record["name"],
        "mapping": plan_record["mapping"],
        "user": client_with_plan.get(
            "/users/{}".format(plan_record["user_id"])
        ).get_json(),
    }
    response = client_with_plan.get("/plans/{}".format(plan_record["id"]))
    assert response.get_json() == expected


def test_single_plan_records_have_users(client_with_plan):
    response = client_with_plan.get("/plans/1")
    assert "user" in response.get_json()


def test_plan_record_is_loadable(plan_record):
    schema = PlanSchema()
    schema.load(plan_record)
