
import flask
import bcrypt
from flask_login import login_required, current_user
from webapp.models import User, UsersLCAccountInfo
from webapp.forms import flash_errors
from webapp.forms import LCAccountInfoForm, MLAccountInfoForm
from webapp.modules.utilities import print_log, encrypt_data, decrypt_data

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
		if form.password.data:
			current_user.enc_password = bcrypt.hashpw(
				password, bcrypt.gensalt()
			)
		try:
			current_user.commit()
			flask.flash("Update success!", 'success')
			return flask.redirect(flask.url_for('settings.ml'))
		except Exception as e:
			flask.flash(str(e), 'danger')

	flash_errors(form)
	return flask.render_template('pages/ml_account.html', form=form)

@settings_blueprint.route('/settings/lc', methods=['get', 'post'])
@login_required
def lc():
	form = LCAccountInfoForm(flask.request.form)
	if flask.request.method == 'GET':
		account_info = UsersLCAccountInfo.get_by_user_id(
			current_user.id
		)
		if account_info:
			#form.api_key.data = account_info.enc_api_key
			form.api_key.data = decrypt_data(
				account_info.enc_api_key,
				current_user.enc_password
			)
			#form.account_number.data = account_info.enc_account_number
			form.account_number.data = decrypt_data(
				account_info.enc_account_number,
				current_user.enc_password
			)
	else:
		if form.validate_on_submit():
			api_key = form.api_key.data
			account_number = form.account_number.data
			new_account_info = UsersLCAccountInfo(
				current_user,
				encrypt_data(api_key, current_user.enc_password),
				encrypt_data(account_number, current_user.enc_password)
			)
			try:
				new_account_info.commit()
				flask.flash("Saved LC account info.", 'success')
				return flask.redirect(flask.url_for('settings.lc'))
			except Exception as e:
				flask.flash(str(e), 'danger')

	flash_errors(form)
	return flask.render_template('pages/lc_account.html', form=form)
