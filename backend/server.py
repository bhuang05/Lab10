from flask import Flask , request , jsonify , send_from_directory
from flask_cors import CORS
import json
import os

app = Flask ( __name__ )
CORS(app)

def load_products():
 with open ( 'products.json', 'r') as f :
        return json.load (f) ['products']
 
@app.route('/products', methods=['GET'])
@app.route('/products/<int:product_id>', methods=['GET'])
def get_products(product_id=None):
    products = load_products()
    if product_id is None:
        # Return all products wrapped in an object with a 'products' key
        return jsonify({"products": products})
    else:
        product = next((p for p in products if p['id'] == product_id), None)
        # If a specific product is requested,
        # wrap it in an object with a 'products' key
        # Note: You might want to change this
        # if you want to return a single product not wrapped in a list
        return jsonify(product) if product else ('', 404)
    
@app.route('/products/add', methods=['POST'])
def add_product():
    new_product = request.json
    products = load_products()
    new_product['id'] = len(products) + 1
    products.append(new_product)
    with open('products.json', 'w') as f:
        json.dump({"products": products}, f)
    return jsonify(new_product), 201

@app.route('/product-images/<path:filename>')
def get_image(filename):
    return send_from_directory('product-images', filename)

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product_details = request.json
    products = load_products()
    for i, product in enumerate(products):
        if product['id'] == product_id:
            products[i].update(product_details)
            with open('products.json', 'w') as f:
                json.dump({"products": products}, f)
            return jsonify(products[i]), 200
    return jsonify({'error': 'Product not found'}), 404
        
@app.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    products = load_products()
    for i, product in enumerate(products):
        if product['id'] == product_id:
            del products[i]
            with open('products.json', 'w') as f:
                json.dump({"products": products}, f)
            return jsonify({'success': 'Product removed'}), 200
    return jsonify({'error': 'Product not found'}), 404




if __name__ == '__main__':
    app.run(debug=True)

