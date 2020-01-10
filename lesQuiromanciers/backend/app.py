import os
import gevent
from flask import Flask
from gevent import pywsgi

# import lesQuiromanciers.routes.global_routes

# app = Flask(__name__, template_folder='./web/templates')
# app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

# app.register_blueprint(lesQuiromanciers.routes.global_routes.app)

# app_server = gevent.pywsgi


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "My_Top_Secert_Key"

    # Blueprint

    from lesQuiromanciers.backend.blueprints.core import bp as bp_core
    bp_core.config(app)

    return app
