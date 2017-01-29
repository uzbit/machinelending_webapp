
from webapp import login_manager
from webapp.models import User
from modules.utilities import print_log

@login_manager.user_loader
def user_loader(user_id):
	user = User.query.filter_by(id=int(user_id)).first()
	#print_log("user_loader - webapp: %s" % str(user))
	return user
