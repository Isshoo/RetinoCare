# server/app/utils/prediction.py
import numpy as np
import os
from keras.models import load_model
from keras.utils import load_img, img_to_array
from PIL import Image # Pillow
from flask import current_app

# --- Configuration ---
BASE_DIR    = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
MODEL_DIR   = os.path.join(BASE_DIR, 'model')
MODEL_NAME  = 'model.h5'
MODEL_PATH  = os.path.join(MODEL_DIR, MODEL_NAME)


MODEL_INPUT_SHAPE = (224, 224) 

CLASSES = ["No DR", "Mild", "Moderate", "Severe", "Proliferative DR"]

# --- Load Model ---
model = None
try:
    if os.path.exists(MODEL_PATH):
        model = load_model(MODEL_PATH)
        print(f"Model '{MODEL_NAME}' loaded successfully from {MODEL_PATH}")
    else:
        print(f"Error: Model file not found at {MODEL_PATH}")
        
except Exception as e:
    print(f"Error loading model: {e}")
    model = None 

def preprocess_image(image_path, target_size):
    """
    Loads and preprocesses an image for model prediction.
    """
    try:
        img = Image.open(image_path)
        
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img = img.resize(target_size)
        img_array = img_to_array(img)
        
        
        img_array = img_array / 255.0 
        

        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        print(f"Error preprocessing image {image_path}: {e}")
        return None

def predict_image(image_path):
    """
    Predicts the class of an image using the loaded Keras model.
    """
    if model is None:
        print("Model is not loaded. Cannot perform prediction.")
        
        return {
            "error": "Model not available",
            "class": "Error",
            "confidence": 0.0,
            "all_confidences": {cls: 0.0 for cls in CLASSES}
        }

    processed_image = preprocess_image(image_path, MODEL_INPUT_SHAPE)
    if processed_image is None:
        return {
            "error": "Image preprocessing failed",
            "class": "Error",
            "confidence": 0.0,
            "all_confidences": {cls: 0.0 for cls in CLASSES}
        }

    try:
        predictions_raw = model.predict(processed_image)[0]  
        
        predicted_index = np.argmax(predictions_raw)
        predicted_class_name = CLASSES[predicted_index]
        highest_confidence = float(predictions_raw[predicted_index])
        
        all_confidences_dict = {cls: float(conf) for cls, conf in zip(CLASSES, predictions_raw)}
        
        return {
            "class": predicted_class_name,
            "confidence": highest_confidence, 
            "all_confidences": all_confidences_dict 
        }
    except Exception as e:
        print(f"Error during model prediction: {e}")
        return {
            "error": "Prediction failed",
            "class": "Error",
            "confidence": 0.0,
            "all_confidences": {cls: 0.0 for cls in CLASSES}
        }
