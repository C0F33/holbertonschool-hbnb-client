from flask import request, jsonify, abort, Blueprint
from model.user import User
from persistence.DataManager import DataManager
from db import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt_identity

user_manager_blueprint = Blueprint('user_manager', __name__)
data_manager = DataManager()


@user_manager_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user is None:
        abort(404, description="User not found")

    if user.is_admin:
        return jsonify(message=f"Welcome, admin {user.first_name}.", user_details={"id": user.id, "email": user.email}), 200
    else:
        return jsonify(message=f"Welcome, regular user {user.first_name}.", user_details={"id": user.id, "email": user.email}), 200


@ user_manager_blueprint.route('/login', methods=['POST'])
def login():
    if not request.json or 'email' not in request.json or 'password' not in request.json:
        abort(400, description="Missing required fields")

    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()

    if user is None:
        abort(401, description="User not found or invalid email")

    if not user.check_password(password):
        abort(401, description="Invalid password")

    additional_claims = {"is_admin": user.is_admin}
    access_token = create_access_token(
        identity=user.id, additional_claims=additional_claims)
    return jsonify(access_token=access_token), 200


@ user_manager_blueprint.route('/users', methods=['POST'])
@ jwt_required()
def create_user():
    claims = get_jwt_identity()
    if not claims.get('is_admin'):
        abort(403, description="Admin rights required")

    if not request.json or 'email' not in request.json or 'password' not in request.json:
        abort(400, description="Missing required fields")

    email = request.json['email']
    if '@' not in email:
        abort(400, description="Invalid email format")

    if User.query.filter_by(email=email).first():
        abort(409, description="Email already exists")

    user = User(
        email=email,
        password=request.json['password'],
        is_admin=request.json.get('is_admin', False),
        password_hash=request.json.get('password_hash', ''),
        first_name=request.json.get('first_name', ''),
        last_name=request.json.get('last_name', '')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created successfully", "user_id": user.id}), 201


@user_manager_blueprint.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user = User.query.get(get_jwt_identity())

    if not user.is_admin:
        abort(403, description="Admin rights required")

    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@ user_manager_blueprint.route('/users/<user_id>', methods=['GET'])
# @jwt_required()
def get_user(user_id):
    # claims = get_jwt_identity()
    # if not claims.get('is_admin'):
    # abort(403, description="Admin rights required")

    user = User.query.get(user_id)
    if user is None:
        abort(404, description="User not found")
    return jsonify(user.to_dict()), 200


@user_manager_blueprint.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(get_jwt_identity())

    if not user.is_admin:
        abort(403, description="Admin rights required")

    user = User.query.get(user_id)
    if user is None:
        abort(404, description="User not found")

    if not request.json:
        abort(400, description="Missing required fields")

    user.email = request.json.get('email', user.email)
    user.first_name = request.json.get('first_name', user.first_name)
    user.last_name = request.json.get('last_name', user.last_name)

    db.session.commit()
    return jsonify(user.to_dict()), 200


@ user_manager_blueprint.route('/users/<user_id>', methods=['DELETE'])
@ jwt_required()
def delete_user(user_id):
    user = User.query.get(get_jwt_identity())

    if not user.is_admin:
        abort(403, description="Admin rights required")

    admin_id = User.query.filter_by(is_admin=True).first().id
    user = User.query.get(user_id)

    if user_id == admin_id:
        abort(403, description="Admin user cannot be deleted")

    if user is None:
        abort(404, description="User not found")

    db.session.delete(user)
    db.session.commit()
    return '', 204
