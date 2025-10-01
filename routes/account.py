from flask import Blueprint, render_template, request, redirect, url_for, session
import os
from db_config import get_db

account_bp = Blueprint('account', __name__)


@account_bp.route('/account')
def account():
    db = get_db()
    user_id = session.get('user', {}).get('id')
    user = db.execute('SELECT * FROM users WHERE id = ?',
                      (user_id,)).fetchone()
    return render_template('account.html', title_website='Account', user=user)
