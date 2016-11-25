import bcrypt
from flask import Blueprint, render_template, request, flash
from flask_login import login_user
from webapp.forms import LoginForm
from webapp.forms import flash_errors
from webapp import login_manager
from webapp.models import User
from webapp.modules.utilities import print_log

login_blueprint = Blueprint('login', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def get_user(username):
	return User.query.filter_by(username=username).first()

def auth_user(user, password):
	encoded = user.password.encode('utf-8')
	return bcrypt.hashpw(password, encoded) == encoded

@login_blueprint.route('/login', methods=['get', 'post'])
def index():
	form = LoginForm(request.form)
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data.encode('utf-8')

		user = get_user(username)
		if user and auth_user(user, password):
			login_user(user)
			return render_template('pages/home.html')
		else:
			flash("Login Error: Wrong username and password combination.")

	flash_errors(form)
	return render_template('forms/login.html', form=form)
