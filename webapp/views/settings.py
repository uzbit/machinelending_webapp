
import flask
from flask_login import login_required, current_user
from webapp.models import UsersLCAccountInfo
from webapp.forms import flash_errors
from webapp.forms import LCAccountInfoForm, MLAccountInfoForm
from webapp.modules.utilities import print_log

settings_blueprint = flask.Blueprint('settings', __name__)

@settings_blueprint.route('/settings', methods=['get', 'post'])
@login_required
def index():
	return flask.render_template('layouts/settings.html')
	# form = LCAccountInfoForm(flask.request.form)
	# if form.validate_on_submit():
	# 	api_key = form.username.data
	# 	password = form.password.data
	#
	# 	flask.flash("Saved.", 'success')
	# 	return flask.redirect(flask.url_for('index.index'))
	# 	# #
	# 	# # user = get_user(username)
	# 	#
	# 	# if user and user.check_password(password):
	# 	# 	login_user(user, remember=True)
	# 	# 	flask.flash("Logged in.", 'success')
	# 	# 	return flask.redirect(flask.url_for('index.index'))
	# 	# else:
	# 	# 	flask.flash("Login Error: Wrong username and password combination.", 'error')
	#
	# flash_errors(form)
	# return flask.redirect(flask.url_for('settings.index'))

@settings_blueprint.route('/settings/ml', methods=['get', 'post'])
@login_required
def ml():
	form = MLAccountInfoForm(flask.request.form)
	form.email.data = current_user.email
	return flask.render_template('pages/ml_account.html', form=form)

@settings_blueprint.route('/settings/lc', methods=['get', 'post'])
@login_required
def lc():
	form = LCAccountInfoForm(flask.request.form)
	if form.validate_on_submit():
		pass

	return flask.render_template('pages/lc_account.html', form=form)
