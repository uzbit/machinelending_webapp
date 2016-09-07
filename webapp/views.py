
from flask import render_template, request
from webapp import app

#----------------------------------------------------------------------------#
# Views.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/lc')
def lc():
    return render_template('pages/lc.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/contact')
def contact():
    return render_template('pages/contact.html')

@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)

@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)



