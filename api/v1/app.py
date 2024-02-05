#!/usr/bin/python3
"""Entry point of the api"""
import os
from flask_cors import CORS
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r'/*':  {'origins': '0.0.0.0'}})

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close_db(exception):
    """Close connection"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """404 error Handler"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    API_HOST = os.getenv('HBNB_API_HOST') or '0.0.0.0'
    API_PORT = os.getenv('HBNB_API_PORT') or 5000
    app.run(host=API_HOST, port=API_PORT, threaded=True)
