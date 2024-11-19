from flask import request, jsonify
from jwt import authentication

from app import app
from app import db
from model.products import Products


@app.route('/novoproduto', methods=['POST'])
def new_product():
    aut = authentication()
    if aut is not None:
        return aut
    
    data = request.get_json()
    new_product = Products(name=data['name'],
                           price=data['price'],
                           qtd=data['qtd'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'id': new_product.id, 'name': new_product.name, 'price': new_product.price, 'qtd': new_product.qtd}), 201


@app.route('/produtos', methods=["GET"])
def list_products():    
    aut = authentication()
    if aut is not None:
        return aut

    productsList = Products.query.all()
    if not productsList:
        return jsonify([]), 200

    
    result = [{'id': product.id, 'name': product.name, 'price': product.price, 'qtd': product.qtd} for product in productsList]


    return jsonify(result)

@app.route('/produtos/<int:product_id>', methods=["GET", "PUT", "DELETE"])
def show_update_delete_product(product_id):
    aut = authentication()
    if aut is not None:
        return aut
        
    product = Products.query.get(product_id)
    if not product:
        return jsonify({'message': 'produto não encontrado'}), 404

    if request.method=="GET":
        return jsonify({'id': product.id, 'name': product.name, 'price': product.price, 'qtd': product.qtd}), 201

    if request.method=="PUT":     
        data = request.get_json()
        product.name = data['name']
        product.price = data['price']
        product.qtd = data['qtd']
        db.session.flush()
        db.session.commit()
        return jsonify({'message': 'produto alterado com sucesso'}), 200


    if request.method=="DELETE":
        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Produto deletado com sucesso!"}), 200