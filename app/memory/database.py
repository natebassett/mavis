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

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    memory_type TEXT DEFAULT 'general',
                    importance INTEGER DEFAULT 1,
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

            connection.commit()