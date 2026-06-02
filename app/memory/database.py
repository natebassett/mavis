import sqlite3
from pathlib import Path

from app.config.config_manager import ConfigManager


class Database:
    def __init__(self):
        self.database_path = ConfigManager.get(
            "DATABASE_PATH",
            "app/memory/mavis.sqlite3"
        )

        Path(self.database_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.initialise_database()

    def connect(self):
        return sqlite3.connect(self.database_path)

    def initialise_database(self):
        with self.connect() as connection:
            cursor = connection.cursor()

            self.create_schema(cursor)
            self.run_migrations(cursor)

            connection.commit()

    def create_schema(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                memory_type TEXT DEFAULT 'general',
                importance INTEGER DEFAULT 1,
                embedding TEXT,
                is_permanent INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                preference_key TEXT NOT NULL UNIQUE,
                preference_value TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    def get_columns(self, cursor, table_name):
        cursor.execute(f"PRAGMA table_info({table_name})")
        return [column[1] for column in cursor.fetchall()]

    def add_column_if_missing(
        self,
        cursor,
        table_name,
        column_name,
        column_definition
    ):
        existing_columns = self.get_columns(cursor, table_name)

        if column_name not in existing_columns:
            cursor.execute(
                f"""
                ALTER TABLE {table_name}
                ADD COLUMN {column_name} {column_definition}
                """
            )

    def run_migrations(self, cursor):
        self.add_column_if_missing(
            cursor,
            "memories",
            "embedding",
            "TEXT"
        )

        self.add_column_if_missing(
            cursor,
            "memories",
            "is_permanent",
            "INTEGER DEFAULT 0"
        )