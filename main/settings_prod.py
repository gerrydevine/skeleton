""" 
Additional Django settings for production project. 
"""

import os
from configparser import ConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Grab protected settings from credentials file
parser = ConfigParser()
parser.read('/etc/pip-curator/prod_settings.py')
secret_key = parser.get('secret', 'SECRETKEY')
db_name = parser.get('database', 'DB_NAME')
db_user = parser.get('database', 'DB_USER')
db_pw = parser.get('database', 'DB_PW')
ip_address = parser.get('ip', 'IP_ADDRESS')
email_user = parser.get('email', 'EMAIL_USER')
email_pw = parser.get('email', 'EMAIL_PW')

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', ip_address]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = secret_key

# Database setup
DATABASES = {
    'default': { 
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': db_name, 
        'USER': db_user, 
        'PASSWORD': db_pw, 
        'HOST': 'localhost', 
        'PORT': '', 
    }
}

# Email setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = email_user
EMAIL_HOST_PASSWORD = email_pw

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
# MEDIA FILES
MEDIA_URL = '/media/'
FILES_DIR = '/srv/media/skeleton'
MEDIA_ROOT = os.path.join(FILES_DIR, 'media')
