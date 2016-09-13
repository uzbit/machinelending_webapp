
from flask import jsonify
from lcApi import app

#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#

@app.route('/lcApi')
def index():
    return jsonify({"hello": "world"})
