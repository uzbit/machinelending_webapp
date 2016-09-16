from flask import Blueprint, render_template, request
from webapp.forms import ForgotForm
forgot_blueprint = Blueprint('forgot', __name__)

@forgot_blueprint.route('/forgot')
def index():
	form = ForgotForm(request.form)
	return render_template('forms/forgot.html', form=form)
