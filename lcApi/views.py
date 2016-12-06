
import os
import cPickle as pickle
import flask
from flask_login import login_required
from flask.views import MethodView
from lcApi import app
from modules.LendingClubApi import LendingClubApi
from modules.utilities import print_log

#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#

class ListedLoansView(MethodView):
	def get(self):
		dataDir = os.path.join(app.config['BASE_DIR'], 'lcApi/data/recentLoans.pickle')
		data = pickle.load(open(dataDir, 'rb'))
		print_log(flask.session)
		return flask.jsonify(data)

	def post(self):
		pass

app.add_url_rule('/listedLoans/', view_func=ListedLoansView.as_view('/listedLoans/'))

class NotesOwnedView(MethodView):
	def get(self):
		if 'api_key' in flask.session \
	 	and 'account_number' in flask.session:
			api_key = flask.session['api_key']
			account_number = flask.session['account_number']
			lcApi = LendingClubApi(
				api_key,
				accountId=account_number,
				test=False
			)
			data = lcApi.getNotesOwned()
			return flask.jsonify({"notesOwned": data})
		return flask.jsonify({})

	def post(self):
		pass

app.add_url_rule('/notesOwned/', view_func=NotesOwnedView.as_view('/notesOwned/'))
