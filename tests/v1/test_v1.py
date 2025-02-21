from http import HTTPStatus

from tests.factories import UserFactory

VERSION_1_ENDPOINT = "/v1"


def test_users(auth_client):
    UserFactory.create_batch(2)

    response = auth_client.get("/v1/users")

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json, list)
    assert len(response.json) == 3


def test_create_user_empty_body(auth_client):
    response = auth_client.post(f"{VERSION_1_ENDPOINT}/users")
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user(auth_client):
    response = auth_client.post(
        f"{VERSION_1_ENDPOINT}/users",
        json={"email": "john.doe@email.com", "first_name": "John", "last_name": "Doe"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json
    assert response.json.get("first_name") == "John"


def test_get_user(auth_client):
    user = UserFactory.create()
    response = auth_client.get(f"{VERSION_1_ENDPOINT}/users/{user.uuid}")
    assert response.status_code == HTTPStatus.OK
    assert response.json
    assert str(user.uuid) == response.json.get("uuid")
