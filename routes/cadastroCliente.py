from flask import request, jsonify
from jwt import authentication

from app import app
from app import db
from model.cadastroCliente import Clientes


@app.route('/novocliente', methods=['POST'])
def new_client():
    aut = authentication()
    if aut is not None:
        return aut
    
    data = request.get_json()
    new_client = Clientes(name=data['name'],
                          cpf=data['cpf'],
                          endereco=data['endereco'],
                          telefone=data['telefone'])
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'id': new_client.id, 'name': new_client.name, 'cpf': new_client.cpf, 'endereco': new_client.endereco, 'telefone': new_client.telefone}), 201


@app.route('/clientes', methods=['GET'])
def show_clientes():
    aut = authentication()
    if aut is not None:
        return aut
    
    clientesList = Clientes.query.all()
    if not clientesList:
        return jsonify([]), 200
    

    result = [{'id': cliente.id, 'name': cliente.name, 'cpf': cliente.cpf, 'endereco': cliente.endereco, 'telefone': cliente.telefone} for cliente in clientesList]

    return jsonify(result)


@app.route('/clientes/<int:cliente_id>', methods=['GET', 'PUT', 'DELETE'])
def show_update_delete_cliente(cliente_id):
    aut = authentication()
    if aut is not None:
        return aut
    
    cliente = Clientes.query.get(cliente_id)
    if not cliente:
        return jsonify({'message': 'Cliente não encontrado'}), 404
    
    if request.method=="GET":
        return jsonify({'id': cliente.id, 'name': cliente.name, 'cpf': cliente.cpf, 'endereco': cliente.endereco, 'telefone': cliente.telefone}), 201
    

    if request.method=="PUT":
        data = request.get_json()
        cliente.name = data['name']
        cliente.cpf = data['cpf']
        cliente.endereco = data['endereco']
        cliente.telefone = data['telefone']
        db.session.flush()
        db.session.commit()
        return jsonify({'message': 'Cadastro alterado com sucesso!'}), 201


    if request.method=="DELETE":
        db.session.delete(cliente)
        db.session.commit()

        return jsonify({"message": 'Cadastro deletado com sucesso!'})