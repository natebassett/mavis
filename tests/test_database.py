from app.memory.database import Database

database = Database()

print("SQLite database initialised successfully.")
print(f"Database path: {database.database_path}")