from flask import Blueprint, render_template

contact_blueprint = Blueprint('contact', __name__)

@contact_blueprint.route('/contact')
def index():
    return render_template('pages/contact.html')
