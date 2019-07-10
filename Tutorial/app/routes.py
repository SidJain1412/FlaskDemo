from app import app
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
    return render_template("hello.html", user=user, title='Home')
