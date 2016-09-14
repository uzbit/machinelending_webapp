from flask import Blueprint, render_template

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login')
def index():
    return render_template('pages/login.html')
