
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from flask import flash

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s field - %s" % (
				getattr(form, field).label.text,
				error
			), 'danger')

class RegisterForm(FlaskForm):
	username = TextField(
		'Username', validators=[DataRequired(), Length(min=4, max=100)]
	)
	email = TextField(
		'Email', validators=[Email(), Length(min=6, max=100)]
	)
	password = PasswordField(
		'Password', validators=[DataRequired(), Length(min=6, max=100)]
	)
	confirm = PasswordField(
		'Repeat Password',
		[DataRequired(),
		EqualTo('password', message='Passwords must match')]
	)
	recaptcha = RecaptchaField()

class MLAccountInfoForm(FlaskForm):
	email = TextField(
		'Email', validators=[Email(), Length(min=6, max=100)]
	)
	password = PasswordField(
		'Password', validators=[DataRequired(), Length(min=6, max=100)]
	)
	confirm = PasswordField(
		'Repeat Password',
		[DataRequired(),
		EqualTo('password', message='Passwords must match')]
	)

class LoginForm(FlaskForm):
	username = TextField('Username', [DataRequired()])
	password = PasswordField('Password', [DataRequired()])

class ForgotForm(FlaskForm):
	email = TextField(
		'Email', validators=[DataRequired(), Length(min=6, max=100)]
	)

class ContactForm(FlaskForm):
	name = TextField('Name', [DataRequired()])
	email = TextField('Email', validators=[Email(), Length(min=3, max=100)])
	comments = TextAreaField('Comments', [DataRequired()])

class LCAccountInfoForm(FlaskForm):
	api_key = TextField('API Key', validators=[Length(min=6, max=100)])
	account_number = TextField('Lending Club Account Number', validators=[Length(min=6, max=100)])
	portfolio_name = TextField('Portfolio Name', validators=[Length(min=0, max=200)])
