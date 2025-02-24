from sqlalchemy.exc import NoResultFound

from app import flask_app
from app.models import User
from config import Config
from tests.factories import UserFactory


def seed_user():
    try:
        User.query.filter_by(api_key=Config.API_KEY).one()
    except NoResultFound:
        UserFactory.create(api_key=Config.API_KEY)

    UserFactory.create_batch(10)


if __name__ == "__main__":
    with flask_app.app_context():
        seed_user()
