import pytest
from flask import testing
from werkzeug.datastructures import Headers

from app import create_app
from app.extensions import db
from config import TestingConfig
from tests.factories import UserFactory

TEST_API_KEY = "11111111-1111-1111-1111-111111111111"


@pytest.fixture(name="application")
def fixture_application():
    """Fixture to set up application with configuration.

    Yields:
        application -- Application context
    """
    app = create_app(TestingConfig)
    flaskapp = app.app

    with flaskapp.app_context(), flaskapp.test_request_context():
        db.drop_all()
        db.create_all()
        yield flaskapp


@pytest.fixture(name="client")
def fixture_client(application):
    """Fixture for HTTP test client.

    Arguments:
        application -- Application context

    Yields:
        client -- HTTP client
    """
    with application.test_client() as c:
        yield c


@pytest.fixture(name="user")
@pytest.mark.usefixtures("application")
def fixture_user():
    yield UserFactory(email="testuser@email.com", api_key=TEST_API_KEY)


class TestClient(testing.FlaskClient):
    def open(self, *args, **kwargs):
        api_key_headers = Headers({"X-Api-Key": self.user.api_key})
        headers = kwargs.pop("headers", Headers())
        headers.extend(api_key_headers)
        kwargs["headers"] = headers
        return super().open(*args, **kwargs)


@pytest.fixture(name="auth_client")
def fixture_auth_client(application, user):
    """Fixture for HTTP test client authenticated.

    Arguments:
        application -- Application context fixture
        user -- API user fixture

    Yields:
        client -- Authenticated client
    """
    TestClient.user = user
    application.test_client_class = TestClient
    with application.test_client() as c:
        yield c
