from app import app
from model.user import *
from model.products import *
from model.lembrete import *


with app.app_context():
    db.create_all()