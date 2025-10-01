from flask import Blueprint, render_template, request, url_for, current_app, redirect, session, jsonify
from db_config import get_db

home_bp = Blueprint('home', __name__)


def cart_count():
    count = 0
    if session.get('cart'):
        for item in session['cart']:
            count += item['quantity']
    return count


def calculate_total_price():
    total = 0
    if session.get('cart'):
        for item in session['cart']:
            total += item['price'] * item['quantity']
    return total


@home_bp.route('/')
def home():
    db = get_db()
    all_products = db.execute('SELECT * FROM products').fetchall()

    return render_template('index.html', title_website='Home', products=all_products, cart_count=cart_count())


@home_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('product_id')
    db = get_db()
    product = db.execute(
        'SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

    if not product:
        return jsonify({'status': 'fail', 'message': 'Không tìm thấy sản phẩm'}), 404

    cart = session.get('cart', [])
    found = False
    new_quantity = 1

    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            new_quantity = item['quantity']
            found = True
            break

    if not found:
        product_data = {
            'id': product['id'],
            'title': product['title'],
            'price': product['price'],
            'image': product['image'],
            'quantity': 1
        }
        cart.append(product_data)

    session['cart'] = cart

    return jsonify({'status': 'success', 'products': session['cart'], 'cart_count': cart_count(), "updated_product": {
        "id": product_id,
        "quantity": new_quantity,
        "total_price": product['price'] * new_quantity
    }, 'total_price': calculate_total_price()}), 200


@home_bp.route('/sub-to-cart', methods=['POST'])
def sub_to_cart():

    product_id = request.json.get('product_id')
    db = get_db()
    product = db.execute(
        'SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

    if not product:
        return jsonify({'status': 'fail', 'message': 'Không tìm thấy sản phẩm'}), 404

    cart = session.get('cart', [])
    new_quantity = 1

    for item in cart:
        if item['id'] == product_id:
            if item['quantity'] <= 1:
                session['cart'] = cart
                return jsonify({'status': 'fail', 'message': 'Số lượng sản phẩm không thể nhỏ hơn 1', 'cart_count': cart_count(), 'total_price': calculate_total_price()}), 400

            item['quantity'] -= 1
            new_quantity = item['quantity']
            break

    session['cart'] = cart

    return jsonify({'status': 'success', 'products': session['cart'], 'cart_count': cart_count(), "updated_product": {
        "id": product_id,
        "quantity": new_quantity,
        "total_price": product['price'] * new_quantity
    }, 'total_price': calculate_total_price()}), 200


@home_bp.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    product_id = request.json.get('product_id')
    db = get_db()
    product = db.execute(
        'SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

    if not product:
        return jsonify({'status': 'fail', 'message': 'Không tìm thấy sản phẩm'}), 404

    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]

    session['cart'] = cart

    return jsonify({'status': 'success', 'products': session['cart'], 'cart_count': cart_count(), 'total_price': calculate_total_price()}), 200


@home_bp.route('/show-cart')
def show_cart():
    cart = session.get('cart', [])
    return render_template('cart.html', products=cart, cart_count=cart_count(), total_price=calculate_total_price())
