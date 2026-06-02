from app.memory.memory_manager import MemoryManager

memory = MemoryManager()

memory_id = memory.add_memory(
    "Nathaniel likes spicy food",
    memory_type="preference",
    importance=3
)

print(f"Added memory with ID: {memory_id}")

print("\nAll memories:")
for item in memory.get_all_memories():
    print(item)

print("\nSearch results for 'spicy':")
for item in memory.search_memories("spicy"):
    print(item)