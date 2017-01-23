import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

BASE_DIR = basedir

# Enable debug mode.
DEBUG = True
TEST = True

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'N5Ovw4avRbwWcSYRb04V'

SENDGRID_API_KEY = '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'

WTF_CSRF_ENABLED = False

RECAPTCHA_PUBLIC_KEY = '6LdixxIUAAAAAPqw4UOohYAXzoZw_swk7zDXkSg7'
RECAPTCHA_PRIVATE_KEY = '6LdixxIUAAAAAI3Q4GHt34KM7TyThAnHfJVeFI5k'

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Application root
#APPLICATION_ROOT = basedir
