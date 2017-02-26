import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

BASE_DIR = basedir

# Enable debug mode.
DEBUG = False
TEST = False

# Secret key for session management. You can generate random strings here:
# http://clsc.net/tools-old/random-string-generator.php
SECRET_KEY = 'N5Ovw4avRbwWcSYRb04V'

SENDGRID_API_KEY = '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'

WTF_CSRF_ENABLED = False

RECAPTCHA_PUBLIC_KEY = '6LdixxIUAAAAAPqw4UOohYAXzoZw_swk7zDXkSg7'
RECAPTCHA_PRIVATE_KEY = '6LdixxIUAAAAAI3Q4GHt34KM7TyThAnHfJVeFI5k'

# Connect to the database
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_DATABASE_URI = 'postgres://qpkczfursjakec:d97c10f3821c1bbb27ca919cd33765abf4fc4cad6c9e9eabecef3891e116e2c3@ec2-54-227-237-223.compute-1.amazonaws.com:5432/d3gtodkddct744'
SQLALCHEMY_TRACK_MODIFICATIONS = True

STRIPE_API_KEY = "sk_test_JeccFfaFc74DYwJ5vQYwsQZK"
# Application root
#APPLICATION_ROOT = basedir
