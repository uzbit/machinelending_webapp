
import os
import cPickle as pickle
import flask
from flask.views import MethodView
from lcApi import app
from modules.LendingClubApi import LendingClubApi
from modules.utilities import print_log

#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#

class LCListedLoansView(MethodView):
	def get(self):
		dataDir = os.path.join(app.config['BASE_DIR'], 'lcApi/data/recentLoans.pickle')
		data = pickle.load(open(dataDir, 'rb'))
		print_log(flask.session)
		return flask.jsonify(data)

	def post(self):
		pass

app.add_url_rule('/listedLoans/', view_func=LCListedLoansView.as_view('/listedLoans/'))
