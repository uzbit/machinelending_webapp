#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
from flask_login import LoginManager
from webapp.models import User
from modules.utilities import print_log
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = None
login_manager.login_message_category = 'danger'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def user_loader(user_id):
	user = User.query.filter_by(id=int(user_id)).first()
	#print_log("user_loader - lcApi: %s" % str(user))
	return user

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

from lcApi import views
