import os
import bcrypt
import flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError, OperationalError

from config import SQLALCHEMY_DATABASE_URI
from webapp import app
from modules.utilities import print_log, encrypt_data, decrypt_data

# engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
# db_session = scoped_session(
# 	sessionmaker(autocommit=True, autoflush=True, bind=engine)
# )
# Base = declarative_base()
# Base.query = db_session.query_property()

db = SQLAlchemy(app)
#db.engine.raw_connection().connection.text_factory = str

# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/
class User(db.Model):
	__tablename__ = 'Users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True)
	email = db.Column(db.String(100), unique=True)
	enc_password = db.Column(db.String(200)) # plain text password of 100 gives enc of 168

	def __init__(self, username, enc_password, email):
		self.username = username
		self.enc_password = enc_password
		self.email = email
		self.authenticated = False
		self.active = True
		self.anonymous = False

	def __repr__(self):
		return '<User %r>' % self.username

	def is_active(self):
		return self.active

	def is_authenticated(self):
		return self.authenticated

	def is_anonymous(self):
		return self.anonymous

	def get_id(self):
		return self.id

	def commit(self):
		db.session.add(self)
		try:
			db.session.commit()
		except IntegrityError as e:
			db.session().rollback()
			print_log(e)
			if str(e).find('constraint failed: Users.username') >= 0:
				raise Exception("Username: %s is already in use." % self.username)
			elif str(e).find('constraint failed: Users.email') >= 0:
				raise Exception("Email: %s is already in use." % self.email)
			else:
				raise Exception("Error in registration.")

	def check_password(self, plaintxt_password):
		plain_encoded = plaintxt_password.encode('utf-8')
		enc_encoded = self.enc_password.encode('utf-8')
		return bcrypt.hashpw(plain_encoded, enc_encoded) == enc_encoded

	@staticmethod
	def get_by_username(username):
		return User.query.filter_by(username=username).first()

class UsersLCAccountInfo(db.Model):
	__tablename__ = 'UsersLCAccountInfo'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
	enc_api_key = db.Column(db.LargeBinary, unique=True)
	enc_account_number = db.Column(db.LargeBinary, unique=True)
	portfolio_name = db.Column(db.String(200))

	def __init__(self, user, enc_api_key, enc_account_number, portfolio_name):
		self.user_id = user.id
		self.enc_api_key = enc_api_key
		self.enc_account_number = enc_account_number
		self.portfolio_name = portfolio_name

	def commit(self):
		db.session.add(self)
		try:
			db.session.commit()
		except IntegrityError as e:
			db.session().rollback()
			print_log(e)

	@staticmethod
	def get_by_user_id(user_id):
		return UsersLCAccountInfo.query.filter_by(user_id=int(user_id)).first()

	@staticmethod
	def decrypt_info(account_info, user):
		api_key, account_number = None, None
		if 'lc_api_key' in flask.session:
			api_key = flask.session['lc_api_key']

		if 'lc_account_number' in flask.session:
			account_number = flask.session['lc_account_number']

		if not api_key and account_info.enc_api_key:
			api_key = decrypt_data(
				account_info.enc_api_key,
				user.enc_password
			)
		if not account_number and account_info.enc_account_number:
			account_number = decrypt_data(
				account_info.enc_account_number,
				user.enc_password
			)
		return api_key, account_number

	@staticmethod
	def get_lc_account_info(user, async=False):
		api_key, account_number = None, None
		account_info = UsersLCAccountInfo.get_by_user_id(
			user.id
		)

		if not account_info:
			account_info = UsersLCAccountInfo(
				user,
				bytes(),
				bytes(),
				''
			)
			return account_info, api_key, account_number

		if async:
			newpid = os.fork()
			if newpid == 0:
				api_key, account_number = UsersLCAccountInfo.decrypt_info(
					account_info,
					user
				)
		else:
			api_key, account_number = UsersLCAccountInfo.decrypt_info(
				account_info,
				user
			)

		flask.session['lc_api_key'] = api_key
		flask.session['lc_account_number'] = account_number
		flask.session['lc_portfolio_name'] = account_info.portfolio_name

		return account_info, api_key, account_number

	@staticmethod
	def update_lc_account_info(
		user, account_info, api_key, account_number
	):
		if account_info:
			flask.session['lc_api_key'] = api_key
			flask.session['lc_account_number'] = account_number
			flask.session['lc_portfolio_name'] = account_info.portfolio_name

			account_info.enc_api_key = encrypt_data(
				api_key, user.enc_password
			)
			account_info.enc_account_number = encrypt_data(
				account_number, user.enc_password
			)
			account_info.commit()

# Create tables.
#Base.metadata.create_all(bind=engine, checkfirst=True)
try:
	#db.drop_all()
	db.create_all()
except OperationalError:
	pass
