from flask import request, jsonify

from app import app
from app import db
from model.lembrete import Lembretes


@app.route('/newlembrete', methods=['POST'])
def create_lembrete():
    data = request.get_json()
    new_lembrete = Lembretes(cliente=data['cliente'],
                            valor=data['valor'],
                            time=data['time'],
                            timer=data['timer'])
    db.session.add(new_lembrete)
    db.session.commit()
    return jsonify({'id': new_lembrete.id, 'cliente': new_lembrete.cliente, 'valor': new_lembrete.valor, 'time': new_lembrete.time, 'timer': new_lembrete.timer}), 201


@app.route('/lembretes', methods=['GET'])
def show_lembretes():
    lembreteList = Lembretes.query.all()
    if not lembreteList:
        return jsonify([]), 200
    

    result = [{'id': lembrete.id, 'cliente': lembrete.cliente, 'valor': lembrete.valor, 'time': lembrete.time, 'timer': lembrete.timer} for lembrete in lembreteList]
    

    return jsonify(result)


@app.route('/lembretes/<int:lembrete_id>', methods=["GET", "PUT", "DELETE"])
def show_update_delete_lembrete(lembrete_id):
    lembrete = Lembretes.query.get(lembrete_id)
    if not lembrete:
        return jsonify({'message': 'Lembrete não encontrado'}), 404
    
    if request.method=="GET":
        return jsonify({'id': lembrete.id, 'cliente': lembrete.cliente, 'valor': lembrete.valor, 'time': lembrete.time, 'timer': lembrete.timer}), 201
    
    if request.method=="PUT":
        data = request.get_json()
        lembrete.cliente = data['cliente']
        lembrete.valor = data['valor']
        lembrete.time = data['time']
        lembrete.timer = data['timer']
        db.session.flush()
        db.session.commit()
        return jsonify({'message': 'Lembrete alterado com sucesso!'}), 201
    
    if request.method=="DELETE":
        db.session.delete(lembrete)
        db.session.commit()

        return jsonify({"message": 'Produto deletado com sucesso!'})