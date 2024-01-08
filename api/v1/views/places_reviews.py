#!/usr/bin/python3
"""new view for reviews of places"""


from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'],
                 strict_slashes=False)
def list_reviews_all(place_id):
    place = storage.get(Place, place_id)
    if place:
        if request.method == 'GET':
            return jsonify(
               [revieweview.to_dict()
                for review in place.reviews
                if place.id == place_id]
                ), 200

        if request.method == 'POST':
            if not request.get_json(silent=True):
                abort(400, 'Not a JSON')
            if not request.get_json(silent=True).get('text'):
                abort(400, 'Missing text')
            if not request.get_json(silent=True).get('user_id'):
                abort(400, 'Missing user_id')
            user_id = request.get_json(silent=True).get('user_id')
            user = storage.get(User, user_id)
            if user is None:
                abort(404)
            new_review = Review(**(request.get_json(silent=True)))
            setattr(new_review, 'place_id', place_id)
            new_review.save()
            return jsonify(new_review.to_dict()), 201

    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_object(review_id):
    """State objects that handles all default RESTFul API actions"""
    review = storage.get(Review, review_id)
    if review:
        if request.method == 'GET':
            return jsonify(review.to_dict()), 200
        elif request.method == 'DELETE':
            storage.delete(review)
            storage.save()
            return {}, 200
        elif request.method == 'PUT':
            if not request.get_json(silent=True):
                abort(400, 'Not a JSON')
            review_update = request.get_json(silent=True)
            if review_update:
                for k, v in review_update.items():
                    if k not in ["id", "created_at", "updated_at",
                                 "user_id", "place_id"]:
                        setattr(review, k, v)
                review.save()
                return jsonify(review.to_dict()), 200
    else:
        abort(404)
