from flask import request, jsonify
from sqlalchemy import asc, desc

from app import app
from model.user import User


@app.route("/users", methods=["GET"])
def list_users():
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