
import flask
import stripe
import urlparse
from flask_login import login_required, current_user
from webapp.models import User
from webapp.forms import flash_errors
from modules.utilities import print_log

stripe.api_key = "sk_test_JeccFfaFc74DYwJ5vQYwsQZK"

subscriptions_blueprint = flask.Blueprint('subscriptions', __name__)

@subscriptions_blueprint.route('/subscriptions', methods=['get', 'post'])
@login_required
def subscriptions():
	if flask.request.method == 'POST':
		try:
			json = urlparse.parse_qs(flask.request.get_data())
			#content = flask.request.get_json(force=True)

			print_log(flask.request.get_data())
			print_log(json)
			customer = stripe.Customer.create(
			  email=json['stripeEmail'],
			  source=json['stripeToken'],
			)
			print_log(customer)
			# stripe.Subscription.create(
  			#	customer=customer.id,
			#	plan="basic-monthly",
			# )
			#current_user.stripeId = customer.id
			#current_user.commit()

			flask.flash("Successfully Subscribed.", 'success')
			return flask.render_template('pages/thankyou_subscriptions.html')
		except Exception as e:
			flask.flash(str(e), 'danger')

	flask.flash("Unable to subscribe!", 'danger')
	return flask.render_template('pages/general_error.html')
