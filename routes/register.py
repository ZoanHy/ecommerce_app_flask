from flask import Blueprint, render_template, request, url_for, current_app, redirect
import re
import os
from werkzeug.security import generate_password_hash
from db_config import get_db

register_bp = Blueprint('register', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE_MB = 1

# kiểm tra email hợp lệ


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


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


@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    errors = {}
    name = ""
    email = ""
    password = ""
    confirm_password = ""
    avatar = ""

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        avatar = request.files.get('avatar')

        if not name:
            errors['name'] = 'Vui lòng nhập tên.'
        if not email:
            errors['email'] = 'Vui lòng nhập email.'
        elif not is_valid_email(email):
            errors['email'] = 'Email không hợp lệ.'

        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu.'
        if not confirm_password:
            errors['confirm_password'] = 'Vui lòng xác nhận mật khẩu.'
        if password and confirm_password and password != confirm_password:
            errors['confirm_password'] = 'Mật khẩu không khớp.'

        file_upload_result = handle_file_upload(avatar)
        if not file_upload_result['success']:
            errors['avatar'] = file_upload_result['error']

        email_exists = get_db().execute(
            'SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if email_exists:
            errors['email'] = 'Email đã được sử dụng.'

        if not errors:
            # ma hoa mat khau
            hashed_password = generate_password_hash(password)

            # luu thong tin nguoi dung vao database
            db = get_db()
            db.execute('INSERT INTO users (name, email, password, avatar) VALUES (?, ?, ?, ?)',
                       (name, email, hashed_password, avatar.filename))
            db.commit()

            # luu avatar vao thu muc uploads
            UPLOAD_FOLDER = os.path.join(current_app.root_path, 'uploads')
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            file_path = os.path.join(UPLOAD_FOLDER, avatar.filename)
            avatar.save(file_path)

            return redirect(url_for('login.login'))

    return render_template('register.html', title_website='Register', errors=errors, name=name, email=email, password=password, avatar=avatar)
