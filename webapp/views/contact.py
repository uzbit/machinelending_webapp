import flask
import datetime
from webapp.forms import ContactForm
from webapp.forms import flash_errors
from modules.utilities import send_email

contact_blueprint = flask.Blueprint('contact', __name__)

@contact_blueprint.route('/contact', methods=['get', 'post'])
def index():
	form = ContactForm(flask.request.form)
	if form.validate_on_submit():
		send_contact_email(form.name.data, form.email.data, form.comments.data)
		return flask.render_template('pages/thankyou_feedback.html')
	flash_errors(form)
	return flask.render_template('pages/contact.html', form=form)

def _get_email(name, email, comments):
	ret = list()
	ret += ["------------------------------------------------------------"]
	ret += ["\tRecieved feedback at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
	ret += ["\t%s (%s) writes: \n" % (name, email)]
	ret += ["\t%s" % comments]
	ret += ["------------------------------------------------------------"]
	return "<br>\n".join(ret)

def send_contact_email(name, email, comments):
	email_body = _get_email(name, email, comments)
	send_email(
		email,
		'guzbit@gmail.com',
		"[Machine Lending] - Contact",
		email_body
	)
