from flask import render_template, jsonify, make_response
from app import app, db
# ERROR HANDLING
# Errors won't be shown if debug=TRUE


# Modifying 404 to send this custom response
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404
# Multiple decorators for more than 1 URL to give the same return


# Internal server error
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# Error handling for bad request
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request. Try again.'}, 400))
