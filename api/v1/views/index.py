#!/usr/bin/python3
""" """
from api.v1.views import app_views


app_views.route("/status")
def display_status:
  """return app_status in JSON format"""
  return '{"status": "OK"}'
