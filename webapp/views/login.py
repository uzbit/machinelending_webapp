from flask import Blueprint, render_template, request
from webapp.forms import LoginForm

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login')
def index():
	form = LoginForm(request.form)
	return render_template('forms/login.html', form=form)
