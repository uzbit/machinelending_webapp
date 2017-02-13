
import os
import cPickle as pickle
import flask
import traceback
from functools import wraps

from config import TEST, STRIPE_API_KEY
from flask.views import MethodView
from flask_login import login_required, current_user
from lcApi import app, login_manager
from modules.LendingClubApi import LendingClubApi
from modules.utilities import print_log, get_order

def user_required(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		if not current_user.is_authenticated:
			return login_manager.unauthorized()
		return f(*args, **kwargs)
	return decorator

def valid_subscription_required(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		print_log(current_user.is_authenticated)
		print_log(current_user.is_subscription_valid())

		if not current_user.is_authenticated:
			return login_manager.unauthorized()

		if not current_user.is_subscription_valid():
			return login_manager.unauthorized()

		return f(*args, **kwargs)
	return decorator

#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#

class ListedLoansView(MethodView):
	def get(self):
		try:
			dataDir = os.path.join(app.config['BASE_DIR'], 'lcApi/data/recentLoans.pickle')
			data = pickle.load(open(dataDir, 'rb'))
			#print_log(flask.session)
			return flask.jsonify(data)
		except Exception as e:
			print_log(traceback.format_exc())
			return flask.jsonify({'error': str(e)})

	def post(self):
		return flask.jsonify({})

app.add_url_rule('/listedLoans/', view_func=ListedLoansView.as_view('/listedLoans/'))

class NotesOwnedView(MethodView):
	def get(self):
		if 'lc_api_key' in flask.session \
		and 'lc_account_number' in flask.session:
			try:
				api_key = flask.session['lc_api_key']
				account_number = flask.session['lc_account_number']
				lcApi = LendingClubApi(
					api_key,
					accountId=account_number,
					test=TEST
				)
				data = lcApi.getNotesOwned()
				return flask.jsonify({"notesOwned": data})
			except Exception as e:
				print_log(traceback.format_exc())
				return flask.jsonify({'error': str(e)})
		return flask.jsonify({})

	def post(self):
		return flask.jsonify({})

view = user_required(NotesOwnedView.as_view('/notesOwned/'))
app.add_url_rule('/notesOwned/', view_func=view)

class AvailableCashView(MethodView):
	def get(self):
		#print_log(flask.session)
		if 'lc_api_key' in flask.session \
		and 'lc_account_number' in flask.session:
			try:
				api_key = flask.session['lc_api_key']
				account_number = flask.session['lc_account_number']
				lcApi = LendingClubApi(
					api_key,
					accountId=account_number,
					test=TEST
				)
				data = lcApi.getAvailableCash()
				return flask.jsonify({'availableCash': data})
			except Exception as e:
				print_log(traceback.format_exc())
				return flask.jsonify({'error': str(e)})
		return flask.jsonify({})

	def post(self):
		return flask.jsonify({})

view = user_required(AvailableCashView.as_view('/availableCash/'))
app.add_url_rule('/availableCash/', view_func=view)

class SubmitOrderView(MethodView):

	def get(self):
		#print_log(flask.session)
		return flask.jsonify({})

	@login_required
	def post(self):
		#print_log(flask.session)
		if 'lc_api_key' in flask.session \
		and 'lc_account_number' in flask.session \
		and 'lc_portfolio_name' in flask.session:
			try:
				api_key = flask.session['lc_api_key']
				account_number = flask.session['lc_account_number']
				portfolio_name = flask.session['lc_portfolio_name']

				lcApi = LendingClubApi(
					api_key,
					accountId=int(account_number),
					test=TEST
				)

				portfolioId = lcApi.getPortfolioId(portfolio_name)
				order = self.__getOrder(portfolioId)
				result = lcApi.placeOrders(order)
				if TEST:
					result = self.__getStubResponse()
				#print_log(result)
				return flask.jsonify(result)
			except Exception as e:
				print_log(traceback.format_exc())
				return flask.jsonify({'error': str(e)})
		return flask.jsonify({})

	def __getStubResponse(self):
		return {
			"orderInstructId":55555,
			"orderConfirmations": [
			{
				"loanId":22222,
				"requestedAmount":55.0,
				"investedAmount":50.0,
				"executionStatus":
					[
					"REQUESTED_AMOUNT_ROUNDED",
					"ORDER_FULFILLED"
					]
			},
			{
				"loanId":33333,
				"requestedAmount":25.0,
				"investedAmount":25.0,
				"executionStatus":
					[
					"ORDER_FULFILLED"
					]
			},
			{
				"loanId":44444,
				"requestedAmount":25.0,
				"investedAmount":0,
				"executionStatus":
					[
					"NOT_AN_INFUNDING_LOAN"
					]
			}]
		}

	def __getOrder(self, portfolioId):
		data = flask.request.form
		order = list()
		for key in data:
			loanId = int(key)
			amount = 25*float(data[key])
			order.append(get_order(loanId, amount, portfolioId))
		return order

view = valid_subscription_required(SubmitOrderView.as_view('/submitOrder/'))
app.add_url_rule('/submitOrder/', view_func=view)
