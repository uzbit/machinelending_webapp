
from flask import render_template, request
from webapp import app

#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')
