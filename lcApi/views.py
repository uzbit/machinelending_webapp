
import os
import cPickle as pickle
from flask import jsonify
from lcApi import app



#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    dataDir = os.path.join(app.config['APPLICATION_ROOT'], 'lcApi/data/recentLoans.pickle')
    data = pickle.load(open(dataDir, 'rb'))
    return jsonify(data)
