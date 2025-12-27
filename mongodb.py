from datetime import datetime
from pymongo import AsyncMongoClient

class Mongodb:
    def __init__(self, connection_string, db_name, collection_name):
        self.client = AsyncMongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        print("Connected to MongoDB")

    async def insert_transaction(self, transaction_data):
        current_time = datetime.now().isoformat() + "Z"
        transaction_data['created_at'] = current_time
        result = await self.collection.insert_one(transaction_data)
        return str(result.inserted_id)

    async def update_transaction(self, transaction_id, update_data):
        result = await self.collection.update_one({"transaction_id": transaction_id}, {"$set": update_data})
        print(f"Updated document count: {result.modified_count}")
        return result.modified_count

    
    async def get_transaction(self, transaction_id):
        # Find by transaction_id field (from payload)
        result = await self.collection.find_one({"transaction_id": transaction_id})
        if result and "_id" in result:
            result["_id"] = str(result["_id"])  # Convert ObjectId to string
        return result

    async def close(self):
        await self.client.close()