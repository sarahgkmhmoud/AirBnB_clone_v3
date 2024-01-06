#!/usr/bin/python3
"""main app"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)


@app.errorhandler(404)
def custom_404(error):
    """handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(self):
    """ remove the current storage"""
    storage.close()


if __name__ == "__main__":
    if getenv('HBNB_API_HOST') and getenv('HBNB_API_PORT'):
        app.run(host=getenv('HBNB_API_HOST'), port=getenv('HBNB_API_PORT'),
                threaded=True)
    else:
        app.run(host='0.0.0.0', port='5000', threaded=True)
