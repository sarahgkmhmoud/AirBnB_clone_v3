#!/usr/bin/python3
"""new view for cities"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET', 'POST'],
                 strict_slashes=False)
def list_cities_all(state_id):
    state = storage.get(State, state_id)
    if state:
        if request.method == 'GET':
            return jsonify(
               [city.to_dict()
                for city in state.cities
                if state.id == state_id]
                ), 200

        if request.method == 'POST':
            if not request.get_json(silent=True):
                abort(400, 'Not a JSON')
            if not request.get_json(silent=True).get('name'):
                abort(400, 'Missing name')
            new_city = City(**(request.get_json(silent=True)))
            setattr(new_city, 'state_id', state_id)
            new_city.save()
            return jsonify(new_city.to_dict()), 201
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_object(city_id):
    """State objects that handles all default RESTFul API actions"""
    city = storage.get(City, city_id)
    if city:
        if request.method == 'GET':
            return jsonify(city.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(city)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            if not request.get_json(silent=True):
                abort(400, 'Not a JSON')
            city_update = request.get_json(silent=True)
            if city_update:
                for k, v in city_update.items():
                    if k not in ["id", "created_at", "updated_at"]:
                        setattr(city, k, v)
                city.save()
                return jsonify(city.to_dict()), 200
    else:
        abort(404)
