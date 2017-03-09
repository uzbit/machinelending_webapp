
import flask
import bcrypt
from flask_login import login_required, current_user
from webapp.models import User, UsersLCAccountInfo
from webapp.forms import flash_errors
from webapp.forms import LCAccountInfoForm, MLAccountInfoForm

settings_blueprint = flask.Blueprint('settings', __name__)

@settings_blueprint.route('/settings', methods=['get', 'post'])
@login_required
def index():
	return flask.render_template('layouts/settings.html')

@settings_blueprint.route('/settings/ml', methods=['get', 'post'])
@login_required
def ml():
	form = MLAccountInfoForm(flask.request.form)
	if flask.request.method == 'GET':
		form.email.data = current_user.email
	if form.validate_on_submit():
		current_user.email = form.email.data
		password = form.password.data.encode('utf-8')
		if password:
			account_info, api_key, account_number = \
				UsersLCAccountInfo.get_lc_account_info(current_user)
			current_user.enc_password = bcrypt.hashpw(
				password, bcrypt.gensalt()
			)
			# Need to update the lc settings...
			try:
				UsersLCAccountInfo.update(
					current_user, account_info, api_key, account_number
				)
			except Exception as e:
				flask.flash(str(e), 'danger')

		try:
			current_user.commit()
			flask.flash("Saved ML account info.", 'success')
			return flask.redirect(flask.url_for('settings.ml'))
		except Exception as e:
			flask.flash(str(e), 'danger')

	flash_errors(form)
	return flask.render_template('pages/ml_account.html', form=form)

@settings_blueprint.route('/settings/lc', methods=['get', 'post'])
@login_required
def lc():
	form = LCAccountInfoForm(flask.request.form)
	account_info, api_key, account_number = \
		UsersLCAccountInfo.get_lc_account_info(current_user)

	if flask.request.method == 'GET':
		form.api_key.data = api_key
		form.account_number.data = account_number
		form.portfolio_name.data = account_info.portfolio_name
	else:
		if form.validate_on_submit():
			api_key = form.api_key.data
			account_number = form.account_number.data
			account_info.portfolio_name = form.portfolio_name.data

			UsersLCAccountInfo.update(
				current_user, account_info, api_key, account_number
			)
			flask.flash("Saved LC account info.", 'success')

	flash_errors(form)
	return flask.render_template('pages/lc_account.html', form=form)
