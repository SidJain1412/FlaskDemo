from app import app, db
from app.forms import LoginForm, RegistrationForm
# Flash for messages, make_response for JSON errors (instead of HTML errors)
from flask import render_template, redirect, flash, make_response, jsonify, url_for, request
# Using HTTPAuth to increase security by protecting through username and p/w
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


# Functions can be protected by adding `@auth.login_required` decorator
auth = HTTPBasicAuth()


# Auth password checker
@auth.get_password
def get_password(username):
    # This could refer to a user database, filler for now
    if(username == "sid"):
        return 'admin'
    return None


# ERROR HANDLING
# Modifying 404 to send this custom response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource Not Found.'}), 404)
# Multiple decorators for more than 1 URL to give the same return


# Error handling for bad request
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request. Try again.'}, 400))


# Error handling for Unauthorized access (Auth)
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}, 403))


# ROUTES
@app.route('/')
@app.route('/index')
# Can't view this page without logging in. Flask login redirects to /login
@login_required
def index():
    return render_template("home.html")


# Using jinja2 templates
@app.route('/hello')
def hello():
    # This data gets passed to hello.html
    posts = [
        {
            'author': {'username': 'Vatsal'},
            'body': 'Chilling in Mumbai'
        },
        {
            'author': {'username': 'Sejal'},
            'body': 'Chilling in Germany'
        }]
    return render_template("hello.html", title='Home', posts=posts)


# Making the login page using forms.py LoginForm class.
# Passing instance of this LoginForm class to the html page
# Browser sends POST request
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in (using flask_login)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # validate_on_submit processes the form. If GET request found then else
    if form.validate_on_submit():
        # Querying the database for user
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            # Flash messages need to be rendered in the redirected page.
            # We add flash support to base.html
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # In case the user has been redirected to the login page from somewhere else:
        # If no next argument in URL, send to index page.
        # .netloc checks if the URL is relative or absolute
        # This is to prevent insertion of some malicious URLs
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Sign In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully.")
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Successfully Registered!")
        return redirect(url_for('login'))
    # Title is going to base.html through register.html
    return render_template('register.html', title="Register", form=form)


# User profile page route:
@app.route('/user/<username>')
@login_required
def user(username):
    # Easy way to check if no user found. Throws 404 if not found.
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test 1'},
        {'author': user, 'body': 'Test 2'}
    ]
    return render_template('user.html', user=user, posts=posts)
