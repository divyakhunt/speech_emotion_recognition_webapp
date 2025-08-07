import numpy as np
import joblib
import tensorflow as tf
from utils import extract_all_features, convert_to_wav

# Load model and preprocessing tools
model = tf.keras.models.load_model("speech_emotion_model.keras")
scaler = joblib.load("scaler.pkl")
encoder = joblib.load("encoder.pkl")

def predict_emotion(audio_path):
    
    # Step 1: Convert to WAV if needed
    wav_path = convert_to_wav(audio_path)

    # Step 2: Extract features from WAV
    features = extract_all_features(audio_path, max_len=300)

    if features.ndim == 2:
        features_flat = features.reshape(-1, features.shape[-1])
        features_scaled = scaler.transform(features_flat)
        features_scaled = features_scaled.reshape(1, features.shape[0], features.shape[1])
    else:
        raise ValueError(f"Expected 2D features (300, 54), got shape: {features.shape}")

    prediction = model.predict(features_scaled)
    predicted_index = np.argmax(prediction)
    predicted_label = encoder.categories_[0][predicted_index]

    return predicted_label
