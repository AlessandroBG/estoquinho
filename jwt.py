from flask import Flask, request, jsonify
import jose
from jose import jwt
from app import app


def generate_jwt(payload):
    token = jwt.encode(payload,
                       app.config['SECRET_KEY'],
                       algorithm=app.config['ALGORITHM'])
    return token


def verify_jwt(token):
    try:
        header, payload, signature = jwt.decode(token,
                                                app.config['SECRET_KEY'],
                                                algorithms=app.config['ALGORITHM'])
        return payload
    except jose.exceptions.JWTError as e:
        print(e)
        return None
    

def authentication():
    authorization = request.headers.get('Authorization')
    if authorization is None:
        return jsonify({'message': "Token is missing"}), 401
    token = authorization.split(' ')[1]
    if not token:
        return jsonify({'message': "Token is missing"}), 401
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'message': "Token is invalid"}), 401
    return None