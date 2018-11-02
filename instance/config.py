import os

# Base configuration


class Config(object):
    DEBUG = False
    TESTING = False
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    DBNAME = os.getenv('DBNAME')
    PASSWORD = os.getenv('PASSWORD')
    USER = os.getenv('USERNAME')

# Test configuration


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    DBNAME = "test_database"

# Development configuration


class DevConfig(Config):
    DEBUG = True

# Production configuration


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProductionConfig
}
