import os
import gevent
from flask import Flask
from gevent import pywsgi

import lesQuiromanciers.routes.RoutesFactory

app = Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(lesQuiromanciers.routes.RoutesFactory.app)

app_server = gevent.pywsgi