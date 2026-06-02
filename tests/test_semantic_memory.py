from app.memory.memory_manager import MemoryManager

memory = MemoryManager()

memory.add_memory(
    "Nathaniel enjoys spicy Korean food",
    memory_type="preference",
    importance=3
)

memory.add_memory(
    "Nathaniel is building MAVIS as a personal AI assistant",
    memory_type="project",
    importance=5
)

memory.add_memory(
    "Nathaniel wants MAVIS to work offline where possible",
    memory_type="project",
    importance=5
)

results = memory.semantic_search_memories(
    "What does Nathaniel want MAVIS to become?"
)

for result in results:
    print(result["content"])
    print("Score:", result["score"])
    print("-" * 30) 