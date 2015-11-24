import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """ Base configuration with values used in all configurations. """

    SERVER_NAME = "localhost:5000"
    SECRET_KEY = os.getenv("MYDICTIONARY_SECRET_KEY")
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WORDS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """
    Development configuration.

    Activates the debugger and uses the database specified
    in the DEV_DATABASE_URL environment variable.

    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("MYDICTIONARY_DEV_DATABASE_URL")
    WORDS_PER_PAGE = 5


class TestingConfig(Config):
    """
    Testing configuration.

    Sets the testing flag to True and uses the database
    specified in the TEST_DATABASE_URL environment variable.

    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("MYDICTIONARY_TEST_DATABASE_URL")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}