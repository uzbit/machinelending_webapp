
import os
import cPickle as pickle
from flask.views import MethodView
from flask import jsonify
from lcApi import app

#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#

class lcApiView(MethodView):
    def get(self):
        dataDir = os.path.join(app.config['BASE_DIR'], 'lcApi/data/recentLoans.pickle')
        data = pickle.load(open(dataDir, 'rb'))
        return jsonify(data)

    def post(self):
        pass

app.add_url_rule('/', view_func=lcApiView.as_view('/'))
