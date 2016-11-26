
import flask
from webapp import app
from webapp.modules.utilities import print_log
from flask_login import current_user

print_log(current_user)
#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return flask.render_template('pages/home.html')
