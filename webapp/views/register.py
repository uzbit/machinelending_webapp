from flask import Blueprint, render_template, request
from webapp.forms import RegisterForm
register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register')
def index():
	form = RegisterForm(request.form)
	return render_template('forms/register.html', form=form)
