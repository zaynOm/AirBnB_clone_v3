#!/usr/bin/python3
"""Entry point of the api"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
import os

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r'/*':  {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exception):
    """Close connection"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    return {"error": "Not found"}, 404


@app.errorhandler(400)
def page_not_found(e):
    message = e.description
    return message, 400


if __name__ == '__main__':
    API_HOST = os.getenv('HBNB_API_HOST') or '0.0.0.0'
    API_PORT = os.getenv('HBNB_API_PORT') or 5000
    app.run(host=API_HOST, port=API_PORT, threaded=True)
