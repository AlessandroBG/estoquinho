from flask import request, jsonify

from app import app
from app import db
from model.lembrete import Lembretes
from model.cadastroCliente import Clientes


@app.route('/newlembrete', methods=['POST'])
def create_lembrete():
    data = request.get_json()
    cliente = db.session.query(Clientes).filter_by(id=data['clienteId']).first()

    if not cliente:
        return jsonify({'error': 'Cliente não encontrado'}), 404

    new_lembrete = Lembretes(
        clienteId=cliente.id,
        clienteName=cliente.name,
        valor=data['valor'],
        time=data['time'],
        timer=data['timer']
    )

    # Adiciona e confirma no banco de dados
    db.session.add(new_lembrete)
    db.session.commit()

    # Retorna os dados do lembrete criado
    return jsonify({
        'id': new_lembrete.id,
        'clienteId': new_lembrete.clienteId,
        'clienteName': new_lembrete.clienteName,
        'valor': new_lembrete.valor,
        'time': new_lembrete.time,
        'timer': new_lembrete.timer
    }), 201


@app.route('/lembretes', methods=['GET'])
def show_lembretes():
    lembreteList = Lembretes.query.all()
    if not lembreteList:
        return jsonify([]), 200
    

    result = [{'id': lembrete.id, 'clienteName': lembrete.clienteName, 'valor': lembrete.valor, 'time': lembrete.time, 'timer': lembrete.timer} for lembrete in lembreteList]
    

    return jsonify(result)


@app.route('/lembretes/<int:lembrete_id>', methods=["GET", "PUT", "DELETE"])
def show_update_delete_lembrete(lembrete_id):
    lembrete = Lembretes.query.get(lembrete_id)
    if not lembrete:
        return jsonify({'message': 'Lembrete não encontrado'}), 404
    
    if request.method=="GET":
        return jsonify({'id': lembrete.id, 'clienteName': lembrete.clienteName,  'valor': lembrete.valor, 'time': lembrete.time, 'timer': lembrete.timer}), 201
    
    
    if request.method=="DELETE":
        db.session.delete(lembrete)
        db.session.commit()

        return jsonify({"message": 'Lembrete deletado com sucesso!'})