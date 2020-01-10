from flask import Blueprint


bp = Blueprint('core', __name__)


def config(app):
    from lesQuiromanciers.backend.blueprints.core import routes # noqa
    app.register_blueprint(bp)