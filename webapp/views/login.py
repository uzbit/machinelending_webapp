
import flask
from flask_login import login_user, login_required
from webapp import login_manager
from webapp.models import db, User
from webapp.forms import LoginForm
from webapp.forms import flash_errors
from webapp.modules.utilities import print_log

login_blueprint = flask.Blueprint('login', __name__)

@login_manager.user_loader
def user_loader(user_id):
	user = User.query.filter_by(id=int(user_id)).first()
	return user

@login_blueprint.route('/login', methods=['get', 'post'])
def index():
	form = LoginForm(flask.request.form)
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data

		user = User.get_by_username(username)

		if user and user.check_password(password):
			login_user(user, remember=True)
			flask.flash("Logged in.", 'success')
			return flask.redirect(flask.url_for('index.index'))
		else:
			flask.flash("Login error: Wrong username and password combination.", 'error')

	flash_errors(form)
	return flask.render_template('pages/login.html', form=form)
