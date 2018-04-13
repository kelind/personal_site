import os

class Configuration(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__)) + '/personal_site'
    DOMAIN = 'http://localhost:5000'
    PRODUCTION_DOMAIN = 'http://kelsilindblad.com'

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/blog.db'.format(APPLICATION_DIR)
    MAKO_TRANSLATE_EXCEPTIONS = False

    SECRET_KEY = 'put a secret key here'
    TOKEN_EXPIRATION = 86400

    STATIC_DIR = APPLICATION_DIR + '/static'

    EMAIL_ENABLED = False
    SMTP_HOST = 'localhost'
    SMTP_USERNAME = 'username'
    SMTP_PASSWORD = 'password'
