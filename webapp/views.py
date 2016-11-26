
import flask
from webapp import app
#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return flask.render_template('pages/home.html')
