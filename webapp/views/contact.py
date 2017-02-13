import flask
import sys
import sendgrid
import datetime
from sendgrid.helpers.mail import *
from config import SENDGRID_API_KEY
from webapp.forms import ContactForm
from webapp.forms import flash_errors

contact_blueprint = flask.Blueprint('contact', __name__)

@contact_blueprint.route('/contact', methods=['get', 'post'])
def index():
	form = ContactForm(flask.request.form)
	if form.validate_on_submit():
		send_email(form.name.data, form.email.data, form.comments.data)
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

def send_email(name, email, comments):
	email_body = _get_email(name, email, comments)
	sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
	from_email = Email(email)
	subject = "[Machine Lending] - Contact"
	to_email = Email("guzbit@gmail.com")
	content = Content("text/html", email_body)
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())
	if response.status_code != 202:
		print "Error sending email:\n%s" % email_body
