import datetime
from flask import request, jsonify
from sqlalchemy import asc, desc
from jwt import generate_jwt, verify_jwt, authentication

from app import app
from app import db
from model.user import User


@app.route("/users", methods=["GET"])
def list_users():
    aut = authentication()
    if aut is not None:
        return aut
    
    users = User.query.all()
    if not users: 
        return jsonify([]), 200

    query_params = request.args

    page = query_params.get('page', default=0, type=int)
    limit = query_params.get('limit', default=10, type=int)
    offset = page * limit

    filter = {}
    ignored_fields = ['page', 'limit', 'sort_by', 'sort_direction']
    for field, value in query_params.items():
        if field not in ignored_fields:
            filter[field] = value

    sort_by = query_params.get('sort_by', default='id', type=str)
    sort_direction = query_params.get('sort_direction', default='asc', type=str)

    order_by = asc(sort_by) if sort_direction == 'asc' else desc(sort_by)

    users = User.query.filter_by(**filter).order_by(order_by).offset(offset).limit(limit).all()
    if not users:
        return jsonify([]), 200

    status_code = 206 if len(users) == limit else 200

    result = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]

    return jsonify(result), status_code


@app.route('/users/<int:user_id>', methods=['GET', 'DELETE'])
def get_user(user_id):
    aut = authentication()
    if aut is not None:
        return aut

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if request.method=="GET":
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
    
    if request.method=="DELETE":
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'],
                    email=data['email'],
                    password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username'],
                                password=data['password']).first()
    if user:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow(),
            "sub": str(user.id)
        }
        token = generate_jwt(payload)
        user_json = {'id': user.id, 'username': user.username, 'email': user.email}
        return jsonify({"token": token, "user": user_json}), 200
    return jsonify({"message": "Invalid username or password"}), 422