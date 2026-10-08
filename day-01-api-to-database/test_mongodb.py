from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")

try:
    client.admin.command("ping")
    print("MongoDB connection successful!")
except Exception as e:
    print("MongoDB connection failed!")
    print(e)
finally:
    client.close()