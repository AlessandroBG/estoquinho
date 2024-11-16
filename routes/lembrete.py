from flask import request, jsonify

from app import app
from app import db
from model.lembrete import Lembretes


@app.route("/create-lembrete", methods=['POST'])
def create_lembrete():
    data = request.get_json()
    new_lembrete = Lembretes(name=data['name'],
                           price=data['price'],
                           qtd=data['qtd'])
    db.session.add(new_lembrete)
    db.session.commit()
    return jsonify({'id': new_lembrete.id, 'cliente': new_lembrete.cliente, 'value': new_lembrete.value, 'time': new_lembrete.time, 'timer': new_lembrete.timer}), 201