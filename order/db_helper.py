from pymongo import AsyncMongoClient
from config_loader import Config


db_url = f"mongodb://{Config.MONGO_HOST}:{Config.MONGO_PORT}/"
CLIENT = AsyncMongoClient(db_url)
DB = CLIENT[Config.MONGO_DB_NAME]
COLLECTION = DB[Config.MONGO_COLLECTION_NAME]


async def test_connection():
    print(f"Number of Collections present: {len(await DB.list_collection_names())}!")


async def close_connection():
    await CLIENT.aclose()
    print("Mongo DB Client closed successfully!")
