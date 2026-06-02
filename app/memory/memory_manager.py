from app.memory.database import Database


class MemoryManager:
    def __init__(self):
        self.database = Database()

    def add_memory(self, content, memory_type="general", importance=1):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO memories (
                    content,
                    memory_type,
                    importance
                )
                VALUES (?, ?, ?)
            """, (content, memory_type, importance))

            connection.commit()

            return cursor.lastrowid

    def get_all_memories(self):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    content,
                    memory_type,
                    importance,
                    created_at
                FROM memories
                ORDER BY created_at DESC
            """)

            return cursor.fetchall()

    def search_memories(self, search_term):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    content,
                    memory_type,
                    importance,
                    created_at
                FROM memories
                WHERE content LIKE ?
                ORDER BY created_at DESC
            """, (f"%{search_term}%",))

            return cursor.fetchall()
    
    def set_preference(self, key, value):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO preferences (
                    preference_key,
                    preference_value
                )
                VALUES (?, ?)
                ON CONFLICT(preference_key)
                DO UPDATE SET
                    preference_value = excluded.preference_value,
                    updated_at = CURRENT_TIMESTAMP
            """, (key, value))

            connection.commit()

    def get_preference(self, key):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT preference_value
                FROM preferences
                WHERE preference_key = ?
            """, (key,))

            result = cursor.fetchone()

            if result:
                return result[0]

            return None

    def get_all_preferences(self):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    preference_key,
                    preference_value,
                    updated_at
                FROM preferences
                ORDER BY preference_key ASC
            """)

            return cursor.fetchall()

    def delete_preference(self, key):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM preferences
                WHERE preference_key = ?
            """, (key,))

            connection.commit()