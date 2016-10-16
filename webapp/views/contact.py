import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Blueprint, render_template, request, flash, url_for, redirect
from webapp.forms import ContactForm

contact_blueprint = Blueprint('contact', __name__)

@contact_blueprint.route('/contact', methods=['get', 'post'])
def index():
	form = ContactForm(request.form)

	if form.validate_on_submit():
		send_email(form.name.data, form.email.data, form.comments.data)
		flash('Thank you for the feedback!')
		return redirect(url_for('index'))
	else:
		print form.errors

	sys.stdout.flush()
	return render_template('pages/contact.html', form=form)

def send_email(name, email, comments):
	msg = MIMEMultipart()
	msg['Subject'] = 'Feedback from machinelending.com'
	msg['From'] = email
	msg['To'] = 'guzbit@gmail.com'
	msg.attach(MIMEText(name+' writes:\n\n'+comments, 'plain'))
	s = smtplib.SMTP()
	s.connect('smtp.gmail.com')
	s.login('guzbit@gmail.com', )

	s.sendmail(email, 'guzbit@gmail.com', msg.as_string())
	s.quit()
