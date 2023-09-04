from datetime import datetime, timezone
from uuid import uuid4

import factory
from faker import Faker
from faker.providers import misc

from app.extensions import db
from app.models import User

fake = Faker()
fake.add_provider(misc)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    email = factory.LazyAttribute(
        lambda this: f"{this.first_name}.{this.last_name}@flaskapi.local".lower()
    )
    uuid = factory.LazyFunction(lambda: uuid4())
    api_key = factory.LazyFunction(lambda: uuid4())
    date_created = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    date_updated = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    enabled = True
