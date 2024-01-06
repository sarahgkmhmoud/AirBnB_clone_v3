#!/usr/bin/python3
""" """
from api.v1.views import app_views
from flask import Flask, jsonify


app_views.route("/status", strict_slashes=False)
def display_status():
  """return app_status in JSON format"""
  return jsonify({"status": "OK"})
