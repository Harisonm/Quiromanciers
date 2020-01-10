import os
import flask
import gevent
from gevent import pywsgi

import lesQuiromanciers.routes.global_routes

app = flask.Flask(__name__, template_folder='./web/templates')
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(lesQuiromanciers.routes.global_routes.app)

app_server = gevent.pywsgi

