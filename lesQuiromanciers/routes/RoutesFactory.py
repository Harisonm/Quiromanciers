import os
import flask
import requests
import time

from lesQuiromanciers.api.wikipedia.WikiFactory import *

app = flask.Blueprint('routes_factory', __name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/wiki/<file_name>', methods=['GET', 'POST'])
def load_data(file_name):
    WikiFactory().build_biographie(file_name)
    print("ok")
    return "Done"