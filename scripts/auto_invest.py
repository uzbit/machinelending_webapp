

from webapp.models import User
from webapp.models import UsersLCInvestParameters
from webapp.models import UsersLCAccountInfo


def auto_invest_for_user(user, account_info):
	print user.stripe_id
	invest_params = UsersLCInvestParameters.get_by_user_id(user.id)
	if invest_params:
		print invest_params

def main():
	users = User.query.all()
	for user in users:
		if not user.stripe_id:
			continue

		account_info = UsersLCAccountInfo.get_by_user_id(user.id)

		if account_info and account_info.auto_invest:
			auto_invest_for_user(user, account_info)

if __name__=="__main__":
	main()
