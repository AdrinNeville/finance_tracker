from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.login'  # if login route is inside a blueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'

    db.init_app(app)
    login_manager.init_app(app)

    from .models import User  # 👈 MUST import User before defining user_loader

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # 👈 This line is what fixes your error

    from .routes import main  # 👈 Blueprint
    app.register_blueprint(main)

    return app