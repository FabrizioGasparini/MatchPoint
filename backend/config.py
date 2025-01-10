import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "Z2gzc3AwOHZvbGxleSE=")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "Z2gzc3AwOHZvbGxleSE=")
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300