import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pymongo import MongoClient
from MadMoney.essentials.env_to_var import env_to_var


class MongoDBClient:
    def __init__(self, database_name="MadMoney", uri=env_to_var("MONGO_URI")):
        self.client = MongoClient(uri)
        self.database = self.client[database_name]

    def insert_one(self, collection_name, document):
        collection = self.database[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def find_one(self, collection_name, query):
        collection = self.database[collection_name]
        return collection.find_one(query)

    def find_many(self, collection_name, query):
        collection = self.database[collection_name]
        return list(collection.find(query))

    def update_one(self, collection_name, query, update):
        collection = self.database[collection_name]
        result = collection.update_one(query, update)
        return result.modified_count

    def delete_one(self, collection_name, query):
        collection = self.database[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count

    def delete_all(self):
        collections = self.database.list_collection_names()
        for collection_name in collections:
            self.database[collection_name].delete_many({})

    def close(self):
        self.client.close()


def main() -> None:
    mongo = MongoDBClient("test")
    mongo.delete_all()
    mongo.close()


if __name__ == "__main__":
    main()
