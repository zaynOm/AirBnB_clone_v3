#!/usr/bin/python3
"""places view"""
from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places_of_city(city_id):
    """display all places of a city"""
    city = storage.get(City, city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])

    abort(404)


@app_views.route('/places/<id>', methods=['GET'])
def place_by_id(id):
    """display place by id"""
    place = storage.get(Place, id)
    if place:
        return place.to_dict()
    abort(404)


@app_views.route('/places/<id>', methods=['DELETE'])
def delete_place(id):
    """delete a place by its id"""
    place = storage.get(Place, id)
    if place:
        storage.delete(place)
        storage.save()
        return {}
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """create a new place"""
    if not storage.get(City, city_id):
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data.get('name'):
        abort(400, 'Missing name')
    if not data.get('user_id'):
        abort(400, 'Missing user_id')
    if not storage.get(User, data.get('user_id')):
        abort(404)
    new_place = Place(city_id=city_id, **data)
    new_place.save()
    return new_place.to_dict(), 201


@app_views.route('/places/<id>', methods=['PUT'])
def update_place(id):
    """update a place by its id"""
    place = storage.get(Place, id)
    if not place:
        return abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    place.save()
    return place.to_dict()


@app_views.route('/places_search', methods=['POST'])
def places_search():
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = set()
    if not states and not cities:
        places = set(storage.all(Place).values())

    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.update(city.places)

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.update(city.places)

    if amenities:
        filtered_places = []
        for place in places:
            place_amenities = [amenity.id for amenity in place.amenities]
            if all(amen in amenities for amen in place_amenities):
                filtered_places.append(place)

        res = []
        for place in filtered_places:
            place_dict = place.to_dict()
            place_dict.pop('amenities')
            res.append(place_dict)

        return jsonify(res)

    return jsonify([place.to_dict() for place in places])
