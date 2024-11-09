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