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
	saveKeys = [x for x in dir(UsersLCInvestParameters) if not x.startswith('_')]
	saveParams = dict()
	for key in saveKeys:
		saveParams[key] = flask.request.form.get(key, 0)

	new_user = UsersLCInvestParameters(
		current_user,
		saveParams
	)
	return flask.render_template('pages/lc.html')
