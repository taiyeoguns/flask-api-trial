from http import HTTPStatus

from tests.factories import UserFactory

VERSION_1_ENDPOINT = "/v1"


def test_users(client):
    UserFactory.create_batch(2)

    response = client.get("/v1/users")

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json, list)
    assert len(response.json) == 2


def test_create_user_empty_body(client):
    response = client.post(f"{VERSION_1_ENDPOINT}/users")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user(client):
    response = client.post(
        f"{VERSION_1_ENDPOINT}/users",
        json={"email": "john.doe@email.com", "first_name": "John", "last_name": "Doe"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json
    assert response.json.get("first_name") == "John"


def test_get_user(client):
    user = UserFactory.create()
    response = client.get(f"{VERSION_1_ENDPOINT}/users/{user.uuid}")
    assert response.status_code == HTTPStatus.OK
    assert response.json
    assert str(user.uuid) == response.json.get("uuid")
