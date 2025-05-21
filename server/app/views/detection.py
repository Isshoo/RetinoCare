from flask import request, jsonify, current_app
from app.models.detection_result import DetectionResult
from app.utils.prediction import predict_image
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User

@jwt_required()
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "Tidak ada file yang diunggah"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "File tidak valid"}), 400
    
    # Validasi ekstensi file
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return jsonify({"error": "Format file tidak didukung"}), 400
    
    # Get user ID from JWT
    user_id = get_jwt_identity()
    if isinstance(user_id, str):
        user_id = int(user_id)
        
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "Pengguna tidak ditemukan"}), 404
    
    # Make sure upload folder exists
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # Simpan file with a secure filename to avoid collisions
    import uuid
    from werkzeug.utils import secure_filename
    
    filename = secure_filename(file.filename)
    # Add unique identifier to prevent overwriting files
    filename = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    
    # Prediksi
    result = predict_image(file_path)
    
    # Simpan ke database
    detection = DetectionResult(
        image_path=file_path,
        result=result,
        user_id=user_id
    )
    db.session.add(detection)
    db.session.commit()
    
    return jsonify({
        "filename": filename,
        "result": result
    }), 200