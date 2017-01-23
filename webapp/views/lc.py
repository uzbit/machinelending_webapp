import flask

lc_blueprint = flask.Blueprint('lc', __name__)

@lc_blueprint.route('/lc')
def index():
    return flask.render_template('pages/lc.html')

# @lc_blueprint.route('/lc/simulate')
# def simulate():
# 	return flask.render_template('pages/lc.html')
#
# @lc_blueprint.route('/lc/invest')
# def invest():
# 	return flask.render_template('pages/lc.html')
