from app import app
from app.forms import LoginForm
# Flash for messages, make_response for JSON errors (instead of HTML errors)
from flask import render_template, redirect, flash, make_response, jsonify
# Using HTTPAuth to increase security by protecting through username and p/w
from flask_httpauth import HTTPBasicAuth

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
    return make_response(jsonify({'error': 'Unauthorized access'}, 401))


# ROUTES
@app.route('/')
@app.route('/index')
def index():
    return render_template("home.html")


# Using jinja2 templates
@app.route('/hello')
def hello():
    # This data gets passed to hello.html
    user = {'username': 'Sid'}
    posts = [
        {
            'author': {'username': 'Vatsal'},
            'body': 'Chilling in Mumbai'
        },
        {
            'author': {'username': 'Sejal'},
            'body': 'Chilling in Germany'
        }]
    return render_template("hello.html", user=user, title='Home', posts=posts)


# Making the login page using forms.py LoginForm class.
# Passing instance of this LoginForm class to the html page
# Browser sends POST request
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # validate_on_submit processes the form. If GET request found then else
    if form.validate_on_submit():
        # Flash messages need to be rendered in the redirected page.
        # We add flash support to base.html
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title="Sign In", form=form)
