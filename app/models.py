from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy_utils import UUIDType

from app import db


class BaseDbModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        UUIDType(),
        index=True,
        unique=True,
        nullable=False,
        default=uuid4,
    )
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    date_updated = db.Column(db.DateTime)
    enabled = db.Column(db.Boolean, default=True, nullable=False)


class User(BaseDbModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), index=True, unique=True, nullable=False)
    api_key = db.Column(
        UUIDType(),
        index=True,
        unique=True,
        nullable=False,
        default=uuid4,
    )
