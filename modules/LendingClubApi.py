import requests, os, json

class LendingClubApi(object):
	API_VERSION = 'v1'

	def __init__(self, apiKey,
			accountId=None,
			test=True,
		):
		self.__apiKey = apiKey
		self.__accountId = str(accountId)
		self.__apiUrlBase = 'https://api.lendingclub.com/api/investor/%s/' % LendingClubApi.API_VERSION
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
			raise Exception(request.reason+" code: %d\nJSON: %s" % (request.status_code, str(request.json())))

	def getRecentLoans(self):
		postfix = 'loans/listing'
		result = self.makeRequest(postfix)
		return result

	def getAllLoans(self):
		postfix = 'loans/listing'
		params = {'showAll': 'true'}
		result = self.makeRequest(postfix, params=params, method="GET")
		return result

	def getNotesOwned(self):
		postfix = 'accounts/%s/notes' % self.__accountId
		return self.makeRequest(postfix)['myNotes']

	def getDetailedNotesOwned(self):
		postfix = 'accounts/%s/detailednotes' % self.__accountId
		return self.makeRequest(postfix)['myNotes']

	def getAvailableCash(self):
		postfix = 'accounts/%s/availablecash' % self.__accountId
		return self.makeRequest(postfix)['availableCash']

	def getPortfolios(self):
		postfix = 'accounts/%s/portfolios' % self.__accountId
		return self.makeRequest(postfix)['myPortfolios']

	def getPortfolioId(self, portfolioName):
		portfolioId = -1
		for portfolio in self.getPortfolios():
			if portfolio['portfolioName'] == portfolioName:
				portfolioId = portfolio['portfolioId']
				break
		return portfolioId

	def getNotes(self):
		postfix = 'accounts/%s/notes' % self.__accountId
		return self.makeRequest(postfix)['myNotes']

	def placeOrders(self, orders):
		params = {
			'aid': self.__accountId,
			'orders': orders
		}
		postfix = 'accounts/%s/orders' % self.__accountId
		if not self.__test:
			return self.makeRequest(postfix, params=params)
		else:
			return params

	def sellNotes(self, order):
		params = order
		params['aid'] = str(self.__accountId)
		postfix = 'accounts/%s/trades/sell' % self.__accountId
		if not self.__test:
			return self.makeRequest(postfix, params=params)
		else:
			return params
