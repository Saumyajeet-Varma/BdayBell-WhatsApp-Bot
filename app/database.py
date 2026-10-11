from pymongo import MongoClient
from pymongo.collection import Collection
from app.config import settings

_clients: MongoClient | None = None
_birthdays: Collection | None = None

def connect_db() -> Collection:
    global _client, _birthdays
    if not settings.mongo_uri:
        raise RuntimeError("MONGO_URI is required")
    _client = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=8000)
    _client.admin.command("ping")
    _birthdays = _client.get_default_database().get_collection("birthdays")
    _birthdays.create_index("date")
    return _birthdays

def get_birthdays_collection() -> Collection:
    if _birthdays is None:
        raise RuntimeError("Database has not been initialized")
    return _birthdays

def close_db() -> None:
    global _client, _birthdays
    if _client is not None:
        _client.close()
    _client = None
    _birthdays = None