import flask
from webapp.models import UsersLCInvestParameters
from modules.utilities import print_log
from flask_login import login_required, current_user

lc_blueprint = flask.Blueprint('lc', __name__)

@lc_blueprint.route('/lc')
def index():
    return flask.render_template('pages/lc.html')

@lc_blueprint.route('/lc/save_invest_params', methods=['post'])
def save_invest_params():
	save_keys = [x for x in dir(UsersLCInvestParameters) if not x.startswith('_')]
	save_params = dict()
	for key in save_keys:
		save_params[key] = flask.request.form.get(key, 0)

	invest_params = UsersLCInvestParameters.get_by_user_id(current_user.id)
	if not invest_params:
		invest_params = UsersLCInvestParameters(
			current_user,
			save_params
		)
		invest_params.commit()
	else:
		UsersLCInvestParameters.update(current_user, save_params)

	return flask.render_template('pages/lc.html')
