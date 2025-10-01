from flask import Flask, render_template, send_from_directory
from db_config import get_db, close_db, init_db
from routes.register import register_bp
from routes.login import login_bp
from routes.logout import logout_bp
from routes.my_product import my_product_bp
from routes.account import account_bp
from routes.home import home_bp

import os

app = Flask(__name__)

# config session
app.secret_key = 'minh huy'

# khoi tao database neu chua co
with app.app_context():
    init_db()


# goi ham close_db sau moi request
app.teardown_appcontext(close_db)

# routes
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(register_bp)
app.register_blueprint(my_product_bp)
app.register_blueprint(account_bp)


@app.route('/add-product')
def add_product():
    return render_template('add-product.html')


@app.route('/404')
def not_found():
    return render_template('404.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/blog-detail')
def blog_detail():
    return render_template('blog-detail.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/contact-us')
def countact_us():
    return render_template('contact-us.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'uploads'), filename)


if __name__ == '__main__':
    app.run(debug=True)
