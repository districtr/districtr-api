import pytest


@pytest.fixture
def plan_record():
    return {"name": "My plan", "serialized": '{"1": 0}'}


def test_create_plan(client, plan_record):
    response = client.post("/plans/", data=plan_record)
    assert response.status_code == 200


def test_created_plan_shows_up_in_list(client, plan_record):
    client.post("/plans/", data=plan_record)
    response = client.get("/plans/")
    assert len(response.get_json()) == 1


def test_hello(client):
    assert client.get("/").data == b"Hello, world!"
