# app.py
from flask import Flask
from flask_login import LoginManager
from finance.models import db, User
from finance.routes import bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(bp)