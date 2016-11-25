import bcrypt
from flask import Blueprint, render_template, request, flash
from webapp.forms import RegisterForm
from webapp.forms import flash_errors
from webapp.modules.utilities import print_log
from webapp.models import User

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['get', 'post'])
def index():
	form = RegisterForm(request.form)
	if form.validate_on_submit():
		password = form.password.data.encode('utf-8')
		newUser = User(
			form.username.data,
			bcrypt.hashpw(password, bcrypt.gensalt()),
			form.email.data
		)
		try:
			newUser.commit_user()
			return render_template('pages/home.html')
		except Exception as e:
			flash(str(e))

	flash_errors(form)
	return render_template('forms/register.html', form=form)
