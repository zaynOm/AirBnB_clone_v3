#!/usr/bin/python3
"""places view"""
from flask import abort, jsonify

from api.v1.views import app_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def amenities_of_place(place_id):
    """display all amenities of a place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify([amenity.to_dict() for amenity in place.amenities])

    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    """Remove an amenity from a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if storage_t == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity.id)

    storage.save()
    return {}


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'])
def link_amenity_place(place_id, amenity_id):
    """Add an amenity to a place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)
    if amenity in place.amenities:
        return amenity.to_dict(), 200

    if storage_t == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)

    storage.save()

    return amenity.to_dict(), 201
