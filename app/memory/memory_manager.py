from app.memory.database import Database
from app.memory.semantic_search import SemanticSearch

class MemoryManager:
    def __init__(self):
        self.database = Database()
        self.semantic_search = SemanticSearch()

    def add_memory(
        self,
        content,
        memory_type="general",
        importance=1,
        is_permanent=False
    ):  
        embedding = self.semantic_search.create_embedding(content)

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO memories (
                    content,
                    memory_type,
                    importance,
                    embedding,
                    is_permanent
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                content,
                memory_type,
                importance,
                embedding,
                int(is_permanent)
            ))

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

    def semantic_search_memories(self, query, limit=5):
        query_embedding_text = self.semantic_search.create_embedding(query)
        query_embedding = self.semantic_search.load_embedding(
            query_embedding_text
        )

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    content,
                    memory_type,
                    importance,
                    embedding,
                    created_at
                FROM memories
                WHERE embedding IS NOT NULL
            """)

            memories = cursor.fetchall()

        scored_memories = []

        for memory in memories:
            memory_id = memory[0]
            content = memory[1]
            memory_type = memory[2]
            importance = memory[3]
            embedding_text = memory[4]
            created_at = memory[5]

            memory_embedding = self.semantic_search.load_embedding(
                embedding_text
            )

            score = self.semantic_search.similarity(
                query_embedding,
                memory_embedding
            )

            scored_memories.append(
                {
                    "id": memory_id,
                    "content": content,
                    "memory_type": memory_type,
                    "importance": importance,
                    "score": score,
                    "created_at": created_at,
                }
            )

        scored_memories.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        return scored_memories[:limit]
    
    # long term methods
    def get_important_memories(self, minimum_importance=4):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    content,
                    memory_type,
                    importance,
                    is_permanent,
                    created_at
                FROM memories
                WHERE importance >= ?
                ORDER BY importance DESC, created_at DESC
            """, (minimum_importance,))

            return cursor.fetchall()

    def get_permanent_memories(self):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    content,
                    memory_type,
                    importance,
                    is_permanent,
                    created_at
                FROM memories
                WHERE is_permanent = 1
                ORDER BY importance DESC, created_at DESC
            """)

            return cursor.fetchall()

    def update_memory(self, memory_id, new_content):
        embedding = self.semantic_search.create_embedding(new_content)

        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE memories
                SET
                    content = ?,
                    embedding = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_content, embedding, memory_id))

            connection.commit()

    def delete_memory(self, memory_id):
        with self.database.connect() as connection:
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM memories
                WHERE id = ?
                AND is_permanent = 0
            """, (memory_id,))

            connection.commit()

            return cursor.rowcount