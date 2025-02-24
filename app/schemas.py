from typing import ClassVar, Type, Optional

from marshmallow import Schema  # noqa
from marshmallow_dataclass import dataclass


@dataclass
class CreateUserInput:
    first_name: str
    last_name: Optional[str]
    email: str

    Schema: ClassVar[Type[Schema]] = Schema  # noqa


@dataclass
class UserResponse:
    first_name: str
    last_name: Optional[str]
    email: str
    uuid: str
    created_at: str

    Schema: ClassVar[Type[Schema]] = Schema  # noqa


@dataclass
class UserListResponse:
    page: int
    per_page: int
    pages: int
    total: int
    users: list[UserResponse]

    Schema: ClassVar[Type[Schema]] = Schema
