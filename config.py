import os
import secrets

try:
    import settings
    TEST_DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_URL = settings.DATABASE_URL
except ImportError:  # pragma: no cover
    TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')
    DATABASE_URL = os.getenv('DATABASE_URL')


class BaseConfig:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(32)  # random string
    AUTH_EXPIRY_TIME_IN_SECONDS = 86400  # token can last a day before it expires


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    AUTH_EXPIRY_TIME_IN_SECONDS = 3  # just 3 seconds and the token expires
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URL


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


app_config = dict(testing=TestingConfig,
                  development=DevelopmentConfig, production=ProductionConfig)
