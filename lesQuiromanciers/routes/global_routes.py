import os
import flask
import requests
import time

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
# CLIENT_SECRETS_FILE = os.environ.get("CLIENT_SECRETS_FILE", default=False)

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.

# SCOPES = ['...']
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'

app = flask.Blueprint('global_routes', __name__)
# Note: A secret key is included in the sample so that it works.
# If you use this code in your application, replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = 'REPLACE ME - this value is here as a placeholder.'

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/home')
def home_page():
    """

    Returns:

    """
    return flask.render_template('home.html')
