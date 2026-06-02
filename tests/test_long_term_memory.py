from app.memory.memory_manager import MemoryManager

memory = MemoryManager()

memory.add_memory(
    "Nathaniel is building MAVIS as a long-term personal AI assistant",
    memory_type="project",
    importance=5,
    is_permanent=True
)

memory.add_memory(
    "Nathaniel likes spicy Korean food",
    memory_type="preference",
    importance=3,
    is_permanent=False
)

memory.add_memory(
    "MAVIS should prioritise privacy and offline functionality",
    memory_type="system_design",
    importance=5,
    is_permanent=True
)

print("Important memories:")
for item in memory.get_important_memories():
    print(item)

print("\nPermanent memories:")
for item in memory.get_permanent_memories():
    print(item)