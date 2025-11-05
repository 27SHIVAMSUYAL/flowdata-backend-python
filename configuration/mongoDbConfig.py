from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()  #.env variables

MONGO_URI = os.getenv("MONGO_URI")
DataBase = os.getenv("DB_NAME")


client = MongoClient(MONGO_URI)

db = client[DataBase]
try:
    client.admin.command('ping')
    print("successfully connected to MongoDB!")
except Exception as e:
    print(e)