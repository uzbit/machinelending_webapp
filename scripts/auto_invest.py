

from webapp.models import User

users = User.query.all()

for user in users:
    print user.stripe_id
