from app import app
from app.forms import LoginForm
from flask import render_template


# Multiple decorators for more than 1 URL to give the same return
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
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Sign In", form=form)
