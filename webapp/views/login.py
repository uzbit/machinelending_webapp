import bcrypt
import flask
from flask_login import login_user, current_user
from webapp import login_manager
from webapp.models import db, User
from webapp.forms import LoginForm
from webapp.forms import flash_errors
from webapp.modules.utilities import print_log

login_blueprint = flask.Blueprint('login', __name__)

def get_user(username):
	user = User.query.filter_by(username=username).first()
	return user

def auth_user(user, password):
	encoded = user.password.encode('utf-8')
	return bcrypt.hashpw(password, encoded) == encoded

@login_manager.user_loader
def user_loader(user_id):
	user = User.query.filter_by(id=int(user_id)).first()
	print_log(user)
	return user

@login_blueprint.route('/login', methods=['get', 'post'])
def index():
	form = LoginForm(flask.request.form)
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data.encode('utf-8')

		user = get_user(username)

		if user and auth_user(user, password):
			login_user(user, remember=True)
			return flask.render_template('forms/login.html', form=form) #flask.redirect(flask.url_for('index.index'))
		else:
			flask.flash("Login Error: Wrong username and password combination.")

	flash_errors(form)
	return flask.render_template('forms/login.html', form=form)
