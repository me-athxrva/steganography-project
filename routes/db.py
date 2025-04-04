from flask.cli import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

mongo = MongoClient(os.getenv('MONGO_URI'))