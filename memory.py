from tinydb import TinyDB, Query

db = TinyDB("mavis_memory.json")
facts = db.table("facts")

def remember(key, value):
    facts.upsert({"key": key, "value": value}, Query().key == key)

def recall(key):
    result = facts.get(Query().key == key)
    return result["value"] if result else None
