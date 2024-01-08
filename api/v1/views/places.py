#!/usr/bin/python3
"""new view for places in a city """


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=['GET', 'POST'],
                 strict_slashes=False)
def list_places_all(city_id):
    city = storage.get(City, city_id)
    if city:
        if request.method == 'GET':
            return jsonify(
               [place.to_dict()
                for place in city.places
                if city.id == city_id]
                ), 200

        if request.method == 'POST':
            if not request.get_json(silent=True):
                abort(400, 'Not a JSON')
            if not request.get_json(silent=True).get('name'):
                abort(400, 'Missing name')
            if not request.get_json(silent=True).get('user_id'):
                abort(400, 'Missing user_id')
            if request.get_json(silent=True).get('user_id') != 'user_id':
                abort(404)
            new_place = Place(**(request.get_json(silent=True)))
            setattr(new_place, 'city_id', city_id)
            new_place.save()
            return jsonify(new_place.to_dict()), 201

    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_object(place_id):
    """State objects that handles all default RESTFul API actions"""
    place = storage.get(Place, place_id)
    if place:
        if request.method == 'GET':
            return jsonify(place.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(place)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            if not request.get_json(silent=True):
                abort(400, 'Not a JSON')
            place_update = request.get_json(silent=True)
            if place_update:
                for k, v in place_update.items():
                    if k not in ["id", "created_at", "updated_at",
                                 "user_id", "city_id"]:
                        setattr(place, k, v)
                place.save()
                return jsonify(place.to_dict()), 200
    else:
        abort(404)
