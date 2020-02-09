"""Default configuration

Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")
WTF_CSRF_ENABLED = False

MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "cloud_manager")
MONGODB_HOST = os.getenv("MONGODB_HOST", "mongodb://localhost")
MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))


# JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
