from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import dynaconf
import jose
from jose import jwt

app = Flask(__name__)
db = SQLAlchemy()
settings = dynaconf.FlaskDynaconf(
    app,
    settings_files=["settings.toml", ".secrets.toml"],
)
db.init_app(app)

import routes