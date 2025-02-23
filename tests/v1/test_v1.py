from http import HTTPStatus

from tests.factories import UserFactory

VERSION_1_ENDPOINT = "/v1"


def test_users_unauthorized(client):
    """Test accessing /v1/users without authentication should return 401 Unauthorized."""
    response = client.get("/v1/users")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_users(auth_client):
    UserFactory.create_batch(2)

    response = auth_client.get("/v1/users")

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json.get("users"), list)
    assert len(response.json.get("users")) == 3


def test_users_pagination(auth_client):
    UserFactory.create_batch(10)

    response = auth_client.get("/v1/users?page=1&per_page=5")

    assert response.status_code == HTTPStatus.OK
    assert isinstance(response.json.get("users"), list)
    assert len(response.json.get("users")) == 5
    assert response.json.get("page") == 1
    assert response.json.get("per_page") == 5
    assert response.json.get("total") == 11


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
