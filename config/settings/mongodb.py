import pymongo

from config.env import env

MONGODB_URL = env("MONGODB_URL", default="mongodb://root:password@localhost:27017")
client = pymongo.MongoClient(MONGODB_URL)

mongodb = client["pizzami_mongodb"]
