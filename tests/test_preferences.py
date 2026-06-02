from app.memory.memory_manager import MemoryManager

memory = MemoryManager()

memory.set_preference("favourite_food", "spicy food")
memory.set_preference("preferred_name", "Nathaniel")
memory.set_preference("wake_word", "MAVIS")

print("Favourite food:")
print(memory.get_preference("favourite_food"))

print("\nAll preferences:")
for preference in memory.get_all_preferences():
    print(preference)

memory.set_preference("favourite_food", "Korean food")

print("\nUpdated favourite food:")
print(memory.get_preference("favourite_food"))