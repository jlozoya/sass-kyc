from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    global client
    if client is None:
        client = AsyncIOMotorClient(settings.MONGODB_URI)
    return client


def get_database():
    mongo_client = get_client()
    return mongo_client[settings.MONGODB_DB_NAME]


def get_collection():
    db = get_database()
    return db["verification_requests"]
