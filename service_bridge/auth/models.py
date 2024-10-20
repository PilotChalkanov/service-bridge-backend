from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from datetime import datetime
import marshmallow_dataclass


class RoleType(Enum):
    USER = "user"
    ADMIN = "admin"


class PaymentMethodType(Enum):
    card = "card"
    cash = "cash"  # Add other payment methods if needed


@dataclass
class BaseUserModel:
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
    phone: str
    created_on: datetime = field(default_factory=datetime.now)
    updated_on: Optional[datetime] = None


@dataclass
class UserModel(BaseUserModel):
    role: RoleType = field(default=RoleType.USER)


UserSchema = marshmallow_dataclass.class_schema(UserModel)


@dataclass
class AdministratorModel(BaseUserModel):
    role: RoleType = field(default=RoleType.ADMIN)


AdministratorSchema = marshmallow_dataclass.class_schema(AdministratorModel)
