from flask import request, jsonify
from sqlalchemy import asc, desc

from app import app
from app import db
from model.products import Products


@app.route('/newproduct', methods=['POST'])
def new_product():
    data = request.get_json()
    new_product = Products(productName=data['productName'],
                           productPrice=data['productPrice'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'id': new_product.id, 'productName': new_product.productName, 'productPrice': new_product.productPrice}), 201


@app.route('/products', methods=["GET"])
def list_products():    
    productsList = Products.query.all()
    if not productsList:
        return jsonify([]), 200

    
    result = [{'id': product.id, 'productName': product.productName, 'productPrice': product.productPrice} for product in productsList]


    return jsonify(result)

@app.route('/products:<int:product_id>', methods=["GET", "PUT", "DELETE"])
def show_update_delete_product(product_id):
    product = Products.query.get(product_id)
    if not product:
        return jsonify({'message': 'produto não encontrado'}), 404

    if request.method=="GET":
        return jsonify({'id': product.id, 'productName': product.productName, 'productPrice': product.productPrice}), 201

    if request.method=="PUT":     
        data = request.get_json()
        product.productName = data['productName']
        product.productPrice = data['productPrice']
        db.session.flush()
        db.session.commit()
        return jsonify({'message': 'produto alterado com sucesso'}), 201


    if request.method=="DELETE":
        db.session.delete(product)
        db.session.commit()

        return jsonify({"message": "Produto deletado com sucesso!"}), 200