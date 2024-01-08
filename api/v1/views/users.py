#!/usr/bin/python3
"""new view for User"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET', 'POST'],
                 strict_slashes=False)
def list_users_all():
    if request.method == 'GET':
        return jsonify([user.to_dict()
                        for user in storage.all(User).values()
                        ]), 200
    if request.method == 'POST':
        if not request.get_json(silent=True):
            abort(400, 'Not a JSON')
        if not request.get_json(silent=True).get('email'):
            abort(400, 'Missing email')
        if not request.get_json(silent=True).get('password'):
            abort(400, 'Missing password')
        new_user = User(**(request.get_json(silent=True)))
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_object(user_id):
    """State objects that handles all default RESTFul API actions"""
    user = storage.get(User, user_id)
    if user:
        if request.method == 'GET':
            return jsonify(user.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(user)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            if not request.get_json(silent=True):
                abort(400, 'Not a JSON')
            user_update = request.get_json(silent=True)
            if user_update:
                for k, v in user_update.items():
                    if k not in ["id", "created_at", "updated_at", "email"]:
                        setattr(user, k, v)
                user.save()
                return jsonify(user.to_dict()), 200
    else:
        abort(404)
