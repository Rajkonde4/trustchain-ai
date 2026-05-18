from pymongo import MongoClient

from app.config.settings import (
    MONGO_URI
)

# CLIENT
client = MongoClient(
    MONGO_URI
)

# DATABASE
db = client["trustchain_ai"]

# COLLECTIONS
users_collection = db["users"]

reports_collection = db[
    "verification_reports"
]