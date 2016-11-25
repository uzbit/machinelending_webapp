
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, Email
from flask import flash

def flash_errors(form):
	for field, errors in form.errors.items():
		for error in errors:
			flash(u"Error in the %s field - %s" % (
				getattr(form, field).label.text,
				error
			))

class RegisterForm(FlaskForm):
	username = TextField(
		'Username', validators=[DataRequired(), Length(min=4, max=50)]
	)
	email = TextField(
		'Email', validators=[Email(), Length(min=6, max=40)]
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
		'Email', validators=[DataRequired(), Length(min=6, max=40)]
	)

class ContactForm(FlaskForm):
	name = TextField('Name', [DataRequired()])
	email = TextField('Email', validators=[Email(), Length(min=0, max=100)])
	comments = TextAreaField('Comments', [DataRequired()])
