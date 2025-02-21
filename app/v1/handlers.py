import logging
from http import HTTPStatus
from typing import Any, Dict

from connexion.exceptions import BadRequestProblem
from connexion.lifecycle import ConnexionResponse
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db, cache
from app.models import User
from app.schemas import CreateUserInput, UserResponse

logger = logging.getLogger(__name__)


@cache.memoize(timeout=60 * 1)
def get_users():
    users = [
        UserResponse(
            first_name=user.first_name,
            last_name=user.last_name,
            uuid=user.uuid,
            email=user.email,
            created_at=user.date_created,
        )
        for user in User.query.all()
    ]

    return UserResponse.Schema().dump(users, many=True)


def get_user(user_id):
    user = None
    try:
        user = User.query.filter_by(uuid=user_id).first()
    except SQLAlchemyError as err:
        if isinstance(err.orig, ValueError):
            raise BadRequestProblem(detail="Invalid UUID provided") from err
        logger.exception(err)

    if user is None:
        return ConnexionResponse(
            body={"message": f"User with ID '{user_id}' not found"},
            status_code=HTTPStatus.NOT_FOUND,
        )

    user_response = UserResponse(
        first_name=user.first_name,
        last_name=user.last_name,
        uuid=user.uuid,
        email=user.email,
        created_at=user.date_created,
    )

    return UserResponse.Schema().dump(user_response)


def create_user(body: Dict[str, Any]) -> Dict[str, Any]:
    try:
        create_user_input: CreateUserInput = CreateUserInput.Schema().load(body)
    except ValidationError as err:
        raise BadRequestProblem(detail=err.messages) from err

    user = User(
        first_name=create_user_input.first_name,
        last_name=create_user_input.last_name,
        email=create_user_input.email,
    )

    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)

    cache.delete_memoized(get_users)

    new_user = UserResponse(
        first_name=user.first_name,
        last_name=user.last_name,
        uuid=user.uuid,
        email=user.email,
        created_at=user.date_created,
    )

    return ConnexionResponse(
        body=UserResponse.Schema().dump(new_user),
        status_code=HTTPStatus.CREATED,
    )
