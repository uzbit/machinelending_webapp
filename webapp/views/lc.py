from flask import Blueprint, render_template

lc_blueprint = Blueprint('lc', __name__)

@lc_blueprint.route('/lc')
def index():
    return render_template('pages/lc.html')
