from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# JSON dosyasından verileri okuma
def read_data():
    with open('products_data.json', 'r') as file:
        data = [json.loads(line) for line in file]
    return data

@app.route('/products', methods=['GET'])
def get_products():
    data = read_data()
    return jsonify(data)

@app.route('/products/<string:name>', methods=['GET'])
def get_product_by_name(name):
    data = read_data()
    product = next((item for item in data if item['name'] == name), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
