from flask import Blueprint, render_template, request
from webapp.forms import RegisterForm
from webapp.forms import flash_errors
from webapp.modules.utilities import print_log
from webapp.models import User


register_blueprint = Blueprint('register', __name__)


@register_blueprint.route('/register', methods=['get', 'post'])
def index():
	form = RegisterForm(request.form)
	if form.validate_on_submit():
		newUser = User(
			form.username.data,
			form.password.data,
			form.email.data
		)
		newUser.commit_user()
		users = User.query.all()
		print_log(users)
		return render_template('pages/home.html')

	flash_errors(form)
	return render_template('forms/register.html', form=form)
