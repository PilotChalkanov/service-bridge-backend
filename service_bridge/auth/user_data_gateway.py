from typing import Optional
from quart import g
from app_factory import db
from auth.models import User


class UserDataGateway:
    @staticmethod
    async def get_user(
        email: str
    ) -> Optional[User]:
        sql = """SELECT * FROM users WHERE email = :email"""
        async with db.connection() as conn:
            record = await conn.fetch_one(sql, {"email": email})
            return User(**dict(record)) if record else None

    @staticmethod
    async def register_user( **kwargs):
        sql = """
                INSERT INTO users (first_name, last_name, email, password, created_on, updated_on)
                VALUES (:first_name, :last_name, :email, :password, :created_on, :updated_on)
            """
        async with g.connection.transaction():
            return await db.execute(sql, **kwargs)

