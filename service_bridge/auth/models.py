from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from app_factory import bcrypt
import marshmallow_dataclass


class RoleType(Enum):
    USER = "user"
    ADMIN = "admin"


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    password: str = field(repr=False)
    id: Optional[int] = None
    created_on: datetime = field(default=datetime.now())
    updated_on: datetime = field(default=datetime.now())

    def __post_init__(self):
        # Hash the password when the object is created
        self.password = bcrypt.generate_password_hash(
            self.password.encode("utf-8")
        ).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


UserSchema = marshmallow_dataclass.class_schema(User)


@dataclass
class AdminUser(User):
    role: RoleType = field(default=RoleType.ADMIN)


AdministratorSchema = marshmallow_dataclass.class_schema(AdminUser)
