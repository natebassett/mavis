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