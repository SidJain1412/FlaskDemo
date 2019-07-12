import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Used to protect against CSRF
    # Check if secret key exists in the environment, else 'admin'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'admin'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
