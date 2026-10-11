from pymongo import MongoClient

client = MongoClient(
    "mongodb://127.0.0.1:27017",
    serverSelectionTimeoutMS=3000,   # fail after 3s instead of the default 30s
)
db = client["day1_engineering"]
tasks_collection = db["tasks"]