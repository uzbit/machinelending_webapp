import bcrypt

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from config import SQLALCHEMY_DATABASE_URI
from webapp import app
from webapp.modules.utilities import print_log

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
db_session = scoped_session(
	sessionmaker(autocommit=True, autoflush=True, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()

db = SQLAlchemy(app)

# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/
class User(Base):
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

class UsersLCAccountInfo(Base):
	__tablename__ = 'UsersLCAccountInfo'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
	enc_api_key = db.Column(db.String(200), unique=True)
	enc_account_number = db.Column(db.String(200), unique=True)

	def __init__(self, user, enc_api_key, enc_account_number):
		self.user_id = user.id
		self.enc_api_key = enc_api_key
		self.enc_account_number = enc_account_number

	def commit(self):
		db.session.add(self)
		try:
			db.session.commit()
		except IntegrityError as e:
			db.session().rollback()
			print_log(e)

	@staticmethod
	def get_by_user_id(user_id):
		return UsersLCAccountInfo.query.filter_by(user_id=user_id).first()

# Create tables.
Base.metadata.create_all(bind=engine)
