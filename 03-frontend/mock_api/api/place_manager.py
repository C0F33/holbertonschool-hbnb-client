from flask import request, jsonify, abort, Blueprint
from model.place import Place
from persistence.DataManager import DataManager
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from model.user import User

place_manager_blueprint = Blueprint('place_manager', __name__)
data_manager = DataManager()


@place_manager_blueprint.route('/place', methods=['POST'])
@jwt_required()
def create_place():
    user = User.query.get(get_jwt_identity())
    if not user.id == Place.query.get(user.id).host_id:
        abort(403, description="owner already exists for this place")

    if not request.json:
        abort(400, description="Missing required fields")

    if Place.query.filter_by(name=request.json.get('name', '')).first():
        abort(409, description="Place already exists")

    place = Place(
        name=request.json.get('name', ''),
        description=request.json.get('description', ''),
        address=request.json.get('address', ''),
        city_id=request.json.get('city_id', ''),
        latitude=request.json.get('latitude', ''),
        longitude=request.json.get('longitude', ''),
        host_id=request.json.get('host_id', ''),
        number_of_rooms=request.json.get('number_of_rooms', ''),
        number_of_bathrooms=request.json.get('number_of_bathrooms', ''),
        price_per_night=request.json.get('price_per_night', ''),
        max_guests=request.json.get('max_guests', ''),
        amenity_ids=request.json.get('amenity_ids', '')
    )
    db.session.add(place)
    db.session.commit()

    return jsonify(place.to_dict()), 201


@place_manager_blueprint.route('/place', methods=['GET'])
@jwt_required()
def get_places():
    user = User.query.get(get_jwt_identity())
    if not user.is_admin:
        abort(403, description="Admin rights required")

    places = Place.query.all()
    places_list = [place.to_dict() for place in places]
    return jsonify(places_list), 200


@place_manager_blueprint.route('/place/<place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        abort(404, description="Place not found")
    return jsonify(place.to_dict()), 200


@place_manager_blueprint.route('/place/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    user = User.query.get(get_jwt_identity())
    if not user.is_admin or not user.id == Place.query.get(place_id).host_id:
        abort(403, description="Admin rights required or owner of the place to edit")

    if not request.json:
        abort(400, description="Missing required fields")

    place = Place.query.get(place_id)
    if not place:
        abort(404, description="Place not found")

    if 'name' in request.json and Place.query.filter_by(name=request.json['name']).first():
        abort(409, description="Place with given name already exists")

    fields_to_update = ['name', 'description', 'address', 'city_id', 'latitude', 'longitude', 'host_id',
                        'number_of_rooms', 'number_of_bathrooms', 'price_per_night', 'max_guests', 'amenity_ids']
    for field in fields_to_update:
        if field in request.json:
            setattr(place, field, request.json[field])

    db.session.commit()
    return jsonify(place.to_dict()), 200


@place_manager_blueprint.route('/place/<place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    user = User.query.get(get_jwt_identity())
    if not user.is_admin or not user.id == Place.query.get(place_id).host_id:
        abort(403, description="Admin rights required or owner of the place to delete")

    place = Place.query.get(place_id)
    if not place:
        abort(404, description="Place not found")

    db.session.delete(place)
    db.session.commit()
    return jsonify({"message": "Place deleted successfully"}), 200
