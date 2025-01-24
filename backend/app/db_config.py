import os
import urllib.parse
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection


class MongoDBClient:

    def __init__(self):
        mongo_host = os.getenv("MONGO_HOST")
        mongo_port = os.getenv("MONGO_PORT")

        mongo_user = urllib.parse.quote_plus(os.getenv("MONGO_USER"))
        mongo_password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

        MONGO_URI = "mongodb://localhost:27017/?replicaSet=rs0"
        DB_NAME = os.getenv("DB_NAME", "task_db")

        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[DB_NAME]

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]
