from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from config import SQLALCHEMY_DATABASE_URI
from webapp import db
from webapp.modules.utilities import print_log

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()

# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.authenticated = False
        self.active = True
        self.anonymous = False

    def __repr__(self):
        return '<User %r>' % self.username

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return self.anonymous

    def commit_user(self):
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

# Create tables.
Base.metadata.create_all(bind=engine)
