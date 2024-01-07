#!/usr/bin/python3
"""new view for State"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities.py", methods=['GET', 'POST'],
                 strict_slashes=False)
def list_amenity_all():
    if request.method == 'GET':
        return jsonify([amenity.to_dict()
                        for amenity in storage.all(Amenity).values()
                        ]), 200
    if request.method == 'POST':
        if not request.get_json(silent=True):
            abort(400, 'Not a JSON')
        if not request.get_json(silent=True).get('name'):
            abort(400, 'Missing name')
        new_state = Amenity(**(request.get_json(silent=True)))
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_object(state_id):
    """State objects that handles all default RESTFul API actions"""
    amenity = storage.get(Amenity, state_id)
    if amenity:
        if request.method == 'GET':
            return jsonify(amenity.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(amenity)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            if not request.get_json(silent=True):
                abort(400, 'Not a JSON')
            state_update = request.get_json(silent=True)
            if state_update:
                for k, v in state_update.items():
                    if k not in ["id", "created_at", "updated_at"]:
                        setattr(amenity, k, v)
                amenity.save()
                return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
