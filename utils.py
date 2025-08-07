import numpy as np
import librosa
import warnings
from pydub import AudioSegment
import os

def convert_to_wav(audio_path):
    
    # Converts an audio file to WAV format if it isn't already.
    # Returns the path to the .wav file.
    
    if audio_path.lower().endswith(".wav"):
        return audio_path

    output_path = os.path.splitext(audio_path)[0] + ".wav"
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_channels(1).set_frame_rate(22050)  # mono & 22.05kHz for consistency
    audio.export(output_path, format="wav")
    return output_path

def extract_all_features(file_path, sr=22050, n_mfcc=40, max_len=300):
    try:
        y, _ = librosa.load(file_path, sr=sr)

        # Skip empty or silent audio
        if y is None or len(y) < 2048 or np.max(np.abs(y)) < 1e-4:
            print(f"Skipped invalid or silent file: {file_path}")
            return np.zeros((max_len, n_mfcc + 12 + 1 + 1))

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)

            # Feature extraction
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc).T
            chroma = librosa.feature.chroma_stft(y=y, sr=sr).T
            zcr = librosa.feature.zero_crossing_rate(y).T
            rms = librosa.feature.rms(y=y).T

        # Make sure all features have the same time steps
        min_len = min(len(mfccs), len(chroma), len(zcr), len(rms))
        mfccs = mfccs[:min_len]
        chroma = chroma[:min_len]
        zcr = zcr[:min_len]
        rms = rms[:min_len]

        combined = np.hstack([mfccs, chroma, zcr, rms])

        # Pad or truncate to fixed length
        if combined.shape[0] < max_len:
            pad_width = max_len - combined.shape[0]
            combined = np.pad(combined, ((0, pad_width), (0, 0)), mode='constant')
        else:
            combined = combined[:max_len]

        return combined

    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return np.zeros((max_len, n_mfcc + 12 + 1 + 1))  # Return zero-padded sequence
