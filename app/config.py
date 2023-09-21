import os
import sqlite3

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def get_database_location():
    return os.environ.get("DATABASE_LOCATION", "/")

def get_port():
    return os.environ.get("PORT", 3000)


