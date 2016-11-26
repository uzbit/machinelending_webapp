import flask

about_blueprint = flask.Blueprint('about', __name__)

@about_blueprint.route('/about')
def index():
    return flask.render_template('pages/about.html')
