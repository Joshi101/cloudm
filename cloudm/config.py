"""Default configuration

Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "cloud_manager")
MONGODB_HOST = os.getenv("MONGODB_HOST", "mongodb://mongodb")
MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))


# JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
