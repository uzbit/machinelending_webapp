import flask
import bcrypt
from webapp.forms import RegisterForm
from webapp.forms import flash_errors
from webapp.modules.utilities import print_log
from webapp.models import User

register_blueprint = flask.Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['get', 'post'])
def index():
	form = RegisterForm(flask.request.form)
	if form.validate_on_submit():
		password = form.password.data.encode('utf-8')
		new_user = User(
			form.username.data,
			bcrypt.hashpw(password, bcrypt.gensalt()),
			form.email.data
		)
		try:
			new_user.commit()
			flask.flash("Registration success!", 'success')
			return flask.redirect(flask.url_for('settings.lc'))
		except Exception as e:
			flask.flash(str(e), 'danger')

	flash_errors(form)
	return flask.render_template('pages/register.html', form=form)
