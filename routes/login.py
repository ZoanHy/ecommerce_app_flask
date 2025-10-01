from flask import Blueprint, render_template, request, session, redirect
from werkzeug.security import check_password_hash
import re
from db_config import get_db
login_bp = Blueprint('login', __name__)


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    errors = {}
    email = ""
    password = ""
    login = ""

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        is_empty = True

        # Validate email
        if not email:
            errors['email'] = 'Email không được để trống.'
            is_empty = False
        elif not is_valid_email(email):
            errors['email'] = 'Email không hợp lệ.'
            is_empty = False

        # Validate password
        if not password:
            errors['password'] = 'Mật khẩu không được để trống.'
            is_empty = False

        if is_empty:

            user_exist = get_db().execute(
                'SELECT id, password FROM users WHERE email = ?', (email,)
            ).fetchone()

            if not user_exist or not check_password_hash(user_exist['password'], password):
                errors['login'] = 'Email hoặc mật khẩu không chính xác!'

        if not errors:
            session.clear()
            session['user'] = {
                'id': user_exist['id'],
                'email': email
            }

            return redirect('/')

    return render_template('login.html', title_website='Login', errors=errors, email=email, password=password)
