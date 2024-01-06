#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage


app_views.route("/status", strict_slashes=False)
def display_status():
    """return app_status in JSON format"""
    return jsonify({"status": "OK"})


app_views.route("/api/v1/stats", strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    return jsonify({"amenities": storage.count(Amenity),
                    "cities": storage.count(City),
                    "places": storage.count(Place),
                    "reviews": storage.count(Review),
                    "states": storage.count(State),
                    "users": storage.count(User)})
