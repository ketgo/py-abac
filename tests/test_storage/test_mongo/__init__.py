import os

from pymongo import MongoClient

DEFAULT_MONGODB_HOST = "127.0.0.1:27017"


def create_client() -> MongoClient:
    host = os.getenv("MONGODB_HOST", DEFAULT_MONGODB_HOST)
    return MongoClient(host)
