from flask import Blueprint, render_template, request
from webapp.forms import RegisterForm
from webapp.forms import flash_errors
from webapp.utilities import print_log
register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['get', 'post'])
def index():
	form = RegisterForm(request.form)
	if form.validate_on_submit():
		print_log(form.name.label.text)

		return render_template('pages/home.html')

	flash_errors(form)
	return render_template('forms/register.html', form=form)
