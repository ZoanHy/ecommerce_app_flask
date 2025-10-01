from flask import Blueprint, render_template, request, redirect, url_for, session
import os
from db_config import get_db

my_product_bp = Blueprint('my_product', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE_MB = 1


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_file_upload(file):
    result = {
        "success": False,
        "error": None,
    }

    # kiem tra file
    if not file or file.filename == '':
        result['error'] = 'Vui lòng chọn ảnh đại diện.'
        return result

    if not allowed_file(file.filename):
        result['error'] = 'Chỉ chấp nhận các định dạng file: png, jpg, jpeg, gif'
        return result

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # reset con tro ve dau file

    if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
        result['error'] = f'Kích thước file không được vượt quá {MAX_FILE_SIZE_MB} MB'
        return result

    result['success'] = True
    return result


@my_product_bp.route('/my-product')
def my_product():
    db = get_db()
    user_id = session.get('user', {}).get('id')
    products = db.execute(
        'SELECT * FROM products WHERE user_id = ?', (user_id,)).fetchall()

    return render_template('my-product.html', title_website='My Products', products=products)


@my_product_bp.route('/add-product', methods=['GET', 'POST'])
def add_product():
    errors = {}
    title = ""
    price = ""
    image = ""

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        price = request.form.get('price', '').strip()
        image = request.files.get('image')

        if not title:
            errors['title'] = 'Vui lòng nhập tên sản phẩm.'
        if not price:
            errors['price'] = 'Vui lòng nhập giá sản phẩm.'
        if not image:
            errors['image'] = 'Vui lòng chọn ảnh sản phẩm.'

        upload_result = handle_file_upload(image)
        if not upload_result['success']:
            errors['image'] = upload_result['error']

        if not errors:
            user_id = session.get('user', {}).get('id')

            db = get_db()
            db.execute(
                'INSERT INTO products (title, price, image, user_id) VALUES (?, ?, ?, ?)',
                (title, price, image.filename, user_id)
            )
            db.commit()

            # luu file
            upload_folder = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), '..', 'uploads')

            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            image_path = os.path.join(upload_folder, image.filename)
            image.save(image_path)

            return redirect(url_for('my_product.my_product'))

    return render_template('add-product.html', title_website='Add Product', errors=errors, title=title, price=price, image=image)


@my_product_bp.route('/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    db = get_db()
    product = db.execute(
        'SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()

    if not product:
        return redirect(url_for('my_product.my_product'))

    errors = {}
    title = ""
    price = ""
    image = ""

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        price = request.form.get('price', '').strip()
        image = request.files.get('image')

        if not title:
            errors['title'] = 'Vui lòng nhập tên sản phẩm.'
        if not price:
            errors['price'] = 'Vui lòng nhập giá sản phẩm.'
        if not image:
            errors['image'] = 'Vui lòng chọn ảnh sản phẩm.'

        upload_result = handle_file_upload(image)
        if not upload_result['success']:
            errors['image'] = upload_result['error']

        if not errors:
            user_id = session.get('user', {}).get('id')

            db = get_db()
            db.execute(
                'UPDATE products SET title = ?, price = ?, image = ? WHERE id = ? AND user_id = ?',
                (title, price, image.filename, product_id, user_id)
            )
            db.commit()

            # luu file
            upload_folder = os.path.join(os.path.dirname(
                os.path.abspath(__file__)), '..', 'uploads')

            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            image_path = os.path.join(upload_folder, image.filename)
            image.save(image_path)

            return redirect(url_for('my_product.my_product'))

    return render_template('edit-product.html', title_website='Edit Product', product=product)


@my_product_bp.route('/delete-product/<int:product_id>')
def delete_product(product_id):
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?', (product_id,))
    db.commit()
    return redirect(url_for('my_product.my_product'))
