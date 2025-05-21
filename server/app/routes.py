from flask import Blueprint, request

bp = Blueprint('main', __name__, url_prefix='/api')

# Add a route handler for OPTIONS requests (preflight)
@bp.route('/auth/login', methods=['OPTIONS'])
def handle_options_login():
    return '', 200

@bp.route('/auth/register', methods=['OPTIONS'])
def handle_options_register():
    return '', 200

@bp.route('/upload', methods=['OPTIONS']) # Add OPTIONS handler for upload
def handle_options_upload():
    return '', 200

# Make sure all your other routes are registered below
from app.views.auth import register, login, logout, refresh
from app.views.detection import upload_image

bp.route('/auth/register', methods=['POST'])(register)
bp.route('/auth/login', methods=['POST'])(login)
bp.route('/auth/logout', methods=['POST'])(logout)
bp.route('/auth/refresh', methods=['POST'])(refresh)
bp.route('/upload', methods=['POST'])(upload_image)