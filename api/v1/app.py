#!/usr/bin/python3
"""main app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)


@app.route("/api/v1/nop", strict_slashes=False)
def custom_404():
    """handler for 404 errors"""
    return jsonify({"error": "Not found"})

@app.teardown_appcontext
def teardown(exception=None):
    """ remove the current storage"""
    storage.close()

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", threaded=True)
