import flask

lc_blueprint = flask.Blueprint('lc', __name__)

@lc_blueprint.route('/lc')
def index():
    return flask.render_template('pages/lc.html')
