import os


class Config(object):
    # Used to protect against CSRF
    # Check if secret key exists in the environment, else 'admin'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'admin'
