from typing import Optional

from auth.database_gateway import DatabaseTemplate
from auth.models import UserModel, UserSchema


class UserDataGateway:
    @staticmethod
    async def get_user(
        username: str, db_template: DatabaseTemplate
    ) -> Optional[UserModel]:
        sql = "SELECT * FROM users WHERE username = $1"
        record = await db_template.fetch_one(sql, username=username)
        return UserSchema.load(dict(record)) if record else None

    @staticmethod
    async def register_user(db_template: DatabaseTemplate, **kwargs):
        sql = """
                INSERT INTO users (username, password, email, first_name, last_name)
                VALUES ($1, $2, $3, $4, $5)
            """
        return await db_template.execute(sql, **kwargs)
