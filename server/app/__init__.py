from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import Config

# Create extensions first
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Updated CORS configuration
    CORS(app,
         origins=["http://localhost:3000"],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
         expose_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
         )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)

    # Import models (after db is defined but before creating tables)
    from app.models.user import User
    from app.models.detection_result import DetectionResult
    
    with app.app_context():
         db.create_all()

    # Register blueprint
    from app.routes import bp
    app.register_blueprint(bp)

    return app

# For Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User  # Import User here to avoid circular imports
    return User.query.get(int(user_id))