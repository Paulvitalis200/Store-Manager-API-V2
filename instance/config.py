import os

# Base configuration


class Config(object):
    DEBUG = False
    SECRET = os.getenv('STOREMANAGER_API_SECRET', 'Imnottellingyou')

# Test configuration


class TestConfig(Config):
    TESTING = True
    DEBUG = True

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
