from flask import Blueprint, render_template, session, redirect

logout_bp = Blueprint('logout', __name__)


@logout_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
