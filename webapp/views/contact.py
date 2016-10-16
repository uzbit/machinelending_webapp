import sys
#import smtplib
#from email.mime.multipart import MIMEMultipart
#from email.mime.text import MIMEText
import datetime

from flask import Blueprint, render_template, request, flash, url_for, redirect
from webapp.forms import ContactForm

contact_blueprint = Blueprint('contact', __name__)

@contact_blueprint.route('/contact', methods=['get', 'post'])
def index():
	form = ContactForm(request.form)

	if form.validate_on_submit():
		write_log(form.name.data, form.email.data, form.comments.data)
		return render_template('pages/thankyou.html')

	return render_template('pages/contact.html', form=form)

def write_log(name, email, comments):
	print "------------------------------------------------------------"
	print "\tRecieved feedback at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print "\t%s (%s) writes: \n" % (name, email)
	print "\t%s" % comments
	print "------------------------------------------------------------"
	sys.stdout.flush()
