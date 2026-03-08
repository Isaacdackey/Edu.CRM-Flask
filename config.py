import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    APP_NAME = os.getenv('APP_NAME', 'MyFlaskApp')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    FLASK_APP = os.getenv('FLASK_APP', 'app.py')
    DEBUG = FLASK_DEBUG
config = Config()