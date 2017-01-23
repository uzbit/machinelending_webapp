import flask
import bcrypt
from flask_login import login_user
from webapp.forms import RegisterForm
from webapp.forms import flash_errors
from webapp.models import User
from modules.utilities import print_log

register_blueprint = flask.Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['get', 'post'])
def index():
	form = RegisterForm(flask.request.form)
	print_log(flask.request.data)
	if form.validate_on_submit():
		password = form.password.data.encode('utf-8')
		new_user = User(
			form.username.data,
			bcrypt.hashpw(password, bcrypt.gensalt()),
			form.email.data
		)
		try:
			new_user.commit()
			login_user(new_user, remember=True)
			flask.flash("Signup complete.", 'success')
			return flask.redirect(flask.url_for('settings.lc'))
		except Exception as e:
			flask.flash(str(e), 'danger')

	flash_errors(form)
	return flask.render_template('pages/register.html', form=form)
