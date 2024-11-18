from datetime import datetime

from flask import request, jsonify
from jwt import authentication

from app import app
from app import db
from model.lembrete import Lembretes
from model.cadastroCliente import Clientes
from model.products import Products


@app.route('/novolembrete', methods=['POST'])
def create_lembrete():
    aut = authentication()
    if aut is not None:
        return aut
    
    data = request.get_json()
    cliente = db.session.query(Clientes).filter_by(id=data['clienteId']).first()
    produto = db.session.query(Products).filter_by(id=data['produtoId']).first()

    date = datetime.now()

    if not cliente:
        return jsonify({'error': 'Cliente não encontrado'}), 404
    
    
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404

    new_lembrete = Lembretes(
        clienteId=cliente.id,
        produtoId=produto.id,
        clienteName=cliente.name,
        produtoName=produto.name,
        valor=produto.price,
        time=date,
    )

    # Adiciona e confirma no banco de dados
    db.session.add(new_lembrete)
    db.session.commit()

    # Retorna os dados do lembrete criado
    return jsonify({
        'id': new_lembrete.id,
        'clienteId': new_lembrete.clienteId,
        'clienteName': new_lembrete.clienteName,
        'produtoName': new_lembrete.produtoName,
        'valor': new_lembrete.valor,
        'time': new_lembrete.time,
    }), 201


@app.route('/lembretes', methods=['GET'])
def show_lembretes():
    aut = authentication()
    if aut is not None:
        return aut
    
    lembreteList = Lembretes.query.all()
    if not lembreteList:
        return jsonify([]), 200
    

    result = [{'id': lembrete.id, 'clienteName': lembrete.clienteName, 'produtoName': lembrete.produtoName, 'valor': lembrete.valor, 'time': lembrete.time} for lembrete in lembreteList]
    

    return jsonify(result)


@app.route('/lembretes/<int:lembrete_id>', methods=["GET", "PUT", "DELETE"])
def show_update_delete_lembrete(lembrete_id):
    aut = authentication()
    if aut is not None:
        return aut
    
    lembrete = Lembretes.query.get(lembrete_id)
    if not lembrete:
        return jsonify({'message': 'Lembrete não encontrado'}), 404
    
    if request.method=="GET":
        return jsonify({'id': lembrete.id, 'clienteName': lembrete.clienteName, 'produtoName': lembrete.produtoName, 'valor': lembrete.valor, 'time': lembrete.time}), 201
    
    
    if request.method=="DELETE":
        db.session.delete(lembrete)
        db.session.commit()

        return jsonify({"message": 'Lembrete deletado com sucesso!'})