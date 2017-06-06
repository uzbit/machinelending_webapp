
import sys
import sendgrid
from sendgrid.helpers.mail import *
from simplecrypt import encrypt, decrypt
from config import SENDGRID_API_KEY

def print_log(out, verbose=True):
    if verbose:
        sys.stdout.write(str(out)+'\n')
    sys.stdout.flush()

def encrypt_data(data, salt):
	return bytes(encrypt(salt, data))

def decrypt_data(data, salt):
	return decrypt(salt, bytes(data)).decode('utf-8')

def get_order(loanId, amount, portfolioId):
	if portfolioId > 0:
		return {
			"loanId": loanId,
			"requestedAmount": amount,
			"portfolioId": portfolioId
		}
	return {}

def get_parameter(kwargs, arg, default):
	return kwargs[arg] if arg in kwargs else default

def send_email(from_email, to_email, subject, body):
	sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
	from_email = Email(from_email)
	to_email = Email(to_email)
	content = Content("text/html", body)
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())
	if response.status_code != 202:
		print "Error sending email:\n%s" % email_body
