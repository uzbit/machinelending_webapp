
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

def get_lc_account_info():
	account_info = UsersLCAccountInfo.get_by_user_id(
		current_user.id
	)
	api_key = None
	account_number = None
	if account_info:
		if account_info.enc_api_key:
			api_key = decrypt_data(
				account_info.enc_api_key,
				current_user.enc_password
			)
		if account_info.enc_account_number:
			account_number = decrypt_data(
				account_info.enc_account_number,
				current_user.enc_password
			)
	return account_info, api_key, account_number

def update_lc_account_info(account_info, api_key, account_number):
	if account_info:
		account_info.enc_api_key = encrypt_data(
			api_key, current_user.enc_password
		)
		account_info.enc_account_number = encrypt_data(
			account_number, current_user.enc_password
		)
		try:
			account_info.commit()
			flask.flash("Saved LC account info.", 'success')
		except Exception as e:
			flask.flash(str(e), 'danger')

@settings_blueprint.route('/settings/ml', methods=['get', 'post'])
@login_required
def ml():
	form = MLAccountInfoForm(flask.request.form)
	if flask.request.method == 'GET':
		form.email.data = current_user.email
	if form.validate_on_submit():
		current_user.email = form.email.data
		password = form.password.data.encode('utf-8')
		# Note, need to invalidate the lc settings...
		if password:
			account_info, api_key, account_number = get_lc_account_info()
			current_user.enc_password = bcrypt.hashpw(
				password, bcrypt.gensalt()
			)
			update_lc_account_info(account_info, api_key, account_number)
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
	account_info, api_key, account_number = get_lc_account_info()
	if flask.request.method == 'GET':
		form.api_key.data = api_key
		form.account_number.data = account_number
	else:
		if form.validate_on_submit():
			if account_info:
				update_lc_account_info(account_info, api_key, account_number)
			else:
				api_key = form.api_key.data
				account_number = form.account_number.data
				account_info = UsersLCAccountInfo(
					current_user,
					bytes(),
					bytes()
				)
				update_lc_account_info(account_info, api_key, account_number)

	flash_errors(form)
	return flask.render_template('pages/lc_account.html', form=form)
