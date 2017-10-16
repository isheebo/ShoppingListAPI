import os
import secrets


class BaseConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(32)  # random string
    AUTH_EXPIRY_TIME_IN_SECONDS = 3600  # 1 hour for the token to expire


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    AUTH_EXPIRY_TIME_IN_SECONDS = 3  # just 3 seconds and the token expires
    SQLALCHEMY_DATABASE_URL = os.getenv(
        'DATABASE_URL', "postgresql://postgres:pumpkin@localhost:5432/ShoppingListTest")


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URL = os.getenv(
        'DATABASE_URL', "postgresql://postgres:pumpkin@localhost:5432/ShoppingList")
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')


app_config = dict(testing=TestingConfig,
                  development=DevelopmentConfig, production=ProductionConfig)
