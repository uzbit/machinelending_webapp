import requests, os, json
import cPickle as pickle

class LendingClubApi(object):
	API_VERSION = 'v1'

	def __init__(self, apiKey,
			accountId=None,
			test=True,
			refresh=True
		):
		self.__apiKey = apiKey
		self.__accountId = accountId
		self.__apiUrlBase = 'https://api.lendingclub.com/api/investor/%s/' % LendingClubApi.API_VERSION
		self.__backupDir = os.path.join(os.path.dirname(__file__), 'backup')
		self.__allLoansPickle = os.path.join(self.__backupDir, 'allLoans.pickle')
		self.__recentLoansPickle = os.path.join(self.__backupDir, 'recentLoans.pickle')
		if not os.path.exists(self.__backupDir):
			os.makedirs(self.__backupDir)

		self.__refresh = refresh
		self.__test = test

	def makeRequest(self, postfix, params=None, method=None):
		headers = {
			'Authorization': self.__apiKey,
			'content-type': 'application/json',
		}
		if not method:
			if params:
				request = requests.post(self.__apiUrlBase + postfix, headers=headers, data=json.dumps(params))
			else:
				request = requests.get(self.__apiUrlBase + postfix, headers=headers)
		elif method == 'POST':
			request = requests.post(self.__apiUrlBase + postfix, headers=headers, params=params)
		elif method == 'GET':
			request = requests.get(self.__apiUrlBase + postfix, headers=headers, params=params)

		if request.status_code == 200:
			return request.json()
		else:
			print request.reason

	def getRecentLoans(self):
		if not self.__refresh and os.path.exists(self.__recentLoansPickle):
			return pickle.load(open(self.__recentLoansPickle, 'rb'))
		postfix = 'loans/listing'
		result = self.makeRequest(postfix)
		pickle.dump(result, open(self.__recentLoansPickle, 'wb'))
		return result

	def getAllLoans(self):
		if not self.__refresh and os.path.exists(self.__allLoansPickle):
			return pickle.load(open(self.__allLoansPickle, 'rb'))
		postfix = 'loans/listing'
		params = {'showAll': 'true'}
		result = self.makeRequest(postfix, params=params, method="GET")
		pickle.dump(result, open(self.__allLoansPickle, 'wb'))
		return result

	def getNotesOwned(self):
		notesOwnedPickle = os.path.join(self.__backupDir, 'notes_owned.pickle')
		if not self.__refresh and os.path.exists(notesOwnedPickle):
			return pickle.load(open(notesOwnedPickle, 'rb'))
		postfix = 'accounts/%s/notes' % self.__accountId
		return self.makeRequest(postfix)['myNotes']

	def getDetailedNotesOwned(self):
		postfix = 'accounts/%s/detailednotes' % self.__accountId
		return self.makeRequest(postfix)['myNotes']

	def getAvailableCash(self):
		postfix = 'accounts/%d/availablecash' % self.__accountId
		return self.makeRequest(postfix)['availableCash']

	def getPortfolios(self):
		postfix = 'accounts/%d/portfolios' % self.__accountId
		return self.makeRequest(postfix)['myPortfolios']

	def getPortfolioId(self, portfolioName):
		portfolioId = -1
		for portfolio in self.getPortfolios():
			if portfolio['portfolioName'] == portfolioName:
				portfolioId = portfolio['portfolioId']
				break
		return portfolioId

	def getNotes(self):
		postfix = 'accounts/%d/notes' % self.__accountId
		return self.makeRequest(postfix)['myNotes']

	def placeOrders(self, orders):
		params = {
			'aid': self.__accountId,
			'orders': orders
		}
		postfix = 'accounts/%d/orders' % self.__accountId
		if not self.__test:
			return self.makeRequest(postfix, params=params)
		else:
			return params

	def sellNotes(self, order):
		params = order
		params['aid'] = str(self.__accountId)
		postfix = 'accounts/%d/trades/sell' % self.__accountId
		if not self.__test:
			return self.makeRequest(postfix, params=params)
		else:
			return params
