from pymongo import MongoClient

client = MongoClient("MONGO_URI")
db = client["ai_vault"]

files_collection = db["files"]