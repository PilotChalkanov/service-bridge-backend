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
    def _format_sql(sql: str, **kwargs: Any) -> str:
        """
        Replaces '?' placeholders in the SQL query with positional placeholders ($1, $2, etc.).
        :param sql: SQL query with '?' as placeholders
        :param kwargs: Dictionary of arguments to replace the placeholders
        :return: Formatted SQL query with $1, $2, etc.
        """
        for index in range(len(kwargs)):
            # Replace '?' with positional placeholders like $1, $2, ...
            sql = sql.replace("?", f"${index + 1}", 1)
        return sql

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
        :param kwargs: Query parameters
        """
        formatted_sql = self._format_sql(sql, **kwargs)
        parsed_sql = self._sub_placeholders(formatted_sql, **kwargs)
        await g.connection.execute(parsed_sql)

    async def fetch_one(self, sql: str, **kwargs: Any) -> Optional[Any]:
        """
        Executes a query and maps the result to a single object if available.
        :param sql: SQL query string
        :param kwargs: Query parameters
        :return: Mapped object or None if no results are found
        """
        formatted_sql = self._format_sql(sql, **kwargs)
        parsed_sql = self._sub_placeholders(formatted_sql, **kwargs)

        return await g.connection.fetch_one(parsed_sql)
