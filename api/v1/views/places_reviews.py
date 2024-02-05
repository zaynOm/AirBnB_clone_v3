#!/usr/bin/python3
"""places review view"""
from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def reviews_of_place(place_id):
    """display all reviews of a place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])

    abort(404)


@app_views.route('/reviews/<id>', methods=['GET'])
def review_by_id(id):
    """display a review by id"""
    review = storage.get(Review, id)
    if review:
        return review.to_dict()
    abort(404)


@app_views.route('/reviews/<id>', methods=['DELETE'])
def delete_review(id):
    """delete a review by its id"""
    review = storage.get(Review, id)
    if review:
        storage.delete(review)
        storage.save()
        return {}
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """create a new place review"""
    if not storage.get(Place, place_id):
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data.get('text'):
        abort(400, 'Missing text')
    if not data.get('user_id'):
        abort(400, 'Missing user_id')
    if not storage.get(User, data.get('user_id')):
        abort(404)
    new_review = Review(place_id=place_id, **data)
    new_review.save()
    return new_review.to_dict(), 201


@app_views.route('/reviews/<id>', methods=['PUT'])
def update_place_review(id):
    """update a place's review by its id"""
    review = storage.get(Review, id)
    if not review:
        return abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    review.save()
    return review.to_dict()
