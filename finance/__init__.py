from flask import Flask
from finance.routes import bp as finance_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'yoursecretkey'
    
    # Register the blueprint
    app.register_blueprint(finance_bp)
    
    return app