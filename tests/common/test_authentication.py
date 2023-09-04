from unittest.mock import patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.common.authentication import validate_user


@pytest.mark.usefixtures("application")
def test_validate_user(user):
    outcome = validate_user(token=user.api_key, required_scopes=None)

    assert outcome.get("uid") == user


@pytest.mark.usefixtures("application")
def test_validate_user_wrong_api_key():
    outcome = validate_user(token=uuid4(), required_scopes=None)

    assert outcome is None


@patch("app.common.authentication.User", autospec=True)
@pytest.mark.usefixtures("application")
def test_validate_user_exception(mock_user):
    mock_user.query.filter_by.side_effect = SQLAlchemyError

    outcome = validate_user(token=uuid4(), required_scopes=None)

    assert outcome is None
