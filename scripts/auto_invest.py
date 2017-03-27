import os
import cPickle as pickle
from lcApi import app
from webapp.models import User
from webapp.models import UsersLCInvestParameters
from webapp.models import UsersLCAccountInfo
from modules.LendingClubApi import LendingClubApi
from modules.utilities import send_email

MAX_TERM = 36
recent_loans = 'lcApi/data/recentLoans.pickle'
recent_loans = pickle.load(open(recent_loans, 'rb'))
loans_date = recent_loans['asOfDate']
recent_loans = recent_loans['loans']

def filter_loan(loan, invest_params):
	if loan['term'] > MAX_TERM: return False
	if loan['intRate'] < invest_params.min_int_rate: return False
	if loan['intRate'] > invest_params.max_int_rate: return False
	if loan['defaultProb'] < invest_params.min_default_rate: return False
	if loan['defaultProb'] > invest_params.max_default_rate: return False
	if loan['loanAmount'] < invest_params.min_loan_amount: return False
	if loan['loanAmount'] > invest_params.max_loan_amount: return False
	return True

def get_order(loan, amount, portfolio_id):
	if portfolio_id > 0:
		return {
			"loanId": loan['id'],
			"requestedAmount": amount,
			"portfolioId": portfolio_id
		}

	return {
		"loanId": loan['id'],
		"requestedAmount": amount,
	}

def place_orders(account_info, api_key, account_number, invest_params):
	lcApi = LendingClubApi(
		api_key, accountId=account_number, test=app.config['TEST']
	)
	portfolio_id = lcApi.getPortfolioId(account_info.portfolio_name)

	filtered_loans = filter(
		lambda x: filter_loan(x, invest_params),
		recent_loans
	)

	notes_owned = lcApi.getNotesOwned()
	owned_ids = [x['loanId'] for x in notes_owned]
	filtered_loans = filter(lambda x: x['id'] not in owned_ids, filtered_loans)

	orders = list()
	for loan in filtered_loans:
		orders.append(get_order(loan, 25, portfolio_id))

	return lcApi.placeOrders(orders)

def format_orderConfirmations(result):
	outText = ''
	if 'orderConfirmations' in result:
		orders = result['orderConfirmations']
		outText = "<table><tr>"
		keys = ['loanId', 'requestedAmount', 'investedAmount',  'executionStatus']

		for key in keys:
			outText += "<th>%s</th>" % key
		outText += "</tr>"
		for order in orders:
			outText += "<tr>"
			for key in keys:
				outText += "<td>%s</td>" % str(order[key])
			outText += "</tr>"
		outText += "</table>"
		outText += "<p>%s</p>" % loans_date
		#[{u'loanId': 99238644, u'executionStatus': [u'NOT_AN_IN_FUNDING_LOAN'], u'investedAmount': 0.0, u'requestedAmount': 25.0}, {u'loanId': 97567829, u'executionStatus': [u'NOT_AN_IN_FUNDING_LOAN'], u'investedAmount': 0.0, u'requestedAmount': 25.0}, {u'loanId': 99607155, u'executionStatus': [u'NOT_AN_IN_FUNDING_LOAN'], u'investedAmount': 0.0, u'requestedAmount': 25.0}, {u'loanId': 99517481, u'executionStatus': [u'NOT_AN_IN_FUNDING_LOAN'], u'investedAmount': 0.0, u'requestedAmount': 25.0}]
	if outText:
		return outText
	else:
		return "No order(s) placed. Attempted to place the following order(s):\n" + str(result)

def auto_invest_for_user(user):
	account_info = UsersLCAccountInfo.get_by_user_id(user.id)
	if not (account_info and account_info.auto_invest):
		return

	api_key, account_number = UsersLCAccountInfo.decrypt_info(account_info, user)

	invest_params = UsersLCInvestParameters.get_by_user_id(user.id)
	if invest_params:
		result = place_orders(
			account_info,
			api_key,
			account_number,
			invest_params
		)

		body = format_orderConfirmations(result)
		body += "<p></p>Parameters used:<br>\n"
		body += "%s" % (str(invest_params))

		send_email(
			'no-reply@machinelending.com',
			user.email,
			'Machine Lending - Auto Invest Report',
			body
		)

def main():
	users = User.query.all()
	for user in users:
		if not user.stripe_id:
			continue

		auto_invest_for_user(user)

if __name__=="__main__":
	main()
