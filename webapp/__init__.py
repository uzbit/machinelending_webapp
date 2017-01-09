#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import logging
import flask

from flask_login import LoginManager, current_user, login_required, logout_user
#from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = flask.Flask(__name__)
app.config.from_object('config')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.index'

#@app.before_request
#def before_request():
#    flask.g.user = current_user

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
	db_session.remove()

# Login required decorator.
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.', 'danger')
			return redirect(url_for('login'))
	return wrap
'''
@app.route("/logout")
@login_required
def logout():
	logout_user()
	flask.flash("Logged out.", 'success')
	return flask.redirect(flask.url_for('index.index'))

# Error handlers.
@app.errorhandler(500)
def internal_error(error):
	#db_session.rollback()
	return flask.render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
	return flask.render_template('errors/404.html'), 404

if not app.debug:
	file_handler = logging.FileHandler('error.log')
	file_handler.setFormatter(
		logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
	)
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

from .views.index import index_blueprint
from .views.lc import lc_blueprint
from .views.about import about_blueprint
from .views.contact import contact_blueprint
from .views.register import register_blueprint
from .views.login import login_blueprint
from .views.forgot import forgot_blueprint
from .views.settings import settings_blueprint

app.register_blueprint(index_blueprint)
app.register_blueprint(lc_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(contact_blueprint)
app.register_blueprint(register_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(forgot_blueprint)
app.register_blueprint(settings_blueprint)
