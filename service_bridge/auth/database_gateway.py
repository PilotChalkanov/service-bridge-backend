from typing import Any, Optional
from quart import g
from quart_db import QuartDB


class DatabaseTemplate:
    def __init__(self, db: QuartDB):
        """
        Initialize the DatabaseTemplate with a connection pool.
        :param db: An asyncpg connection pool
        """
        self.db = db

    @staticmethod
    def _sub_placeholders(sql: str, **columns: str) -> str:
        """
        Replaces positional placeholders ($1, $2, etc.) in the SQL query with actual column names.

        :param sql: SQL query with positional placeholders ($1, $2, etc.)
        :param columns: Dictionary of actual column names to substitute for the placeholders
        :return: Formatted SQL query with actual column names
        """
        for i, col in enumerate(columns.values()):
            sql = sql.replace(f"${i + 1}", f"'{col}'", 1)
        return sql

    async def execute(self, sql: str, **kwargs: Any) -> None:
        """
        Executes an SQL command (e.g., INSERT, UPDATE, DELETE) with the provided arguments.
        :param sql: SQL query string
        :param kwargs: Query parameters"""

        parsed_sql = self._sub_placeholders(sql, **kwargs)
        await g.connection.execute(parsed_sql)

    async def fetch_one(self, sql: str, **kwargs: Any) -> Optional[Any]:
        """
        Executes a query and maps the result to a single object if available.
        :param sql: SQL query string
        :param kwargs: Query parameters
        :return: Mapped object or None if no results are found
        """
        parsed_sql = self._sub_placeholders(sql, **kwargs)
        return await g.connection.fetch_one(parsed_sql)
