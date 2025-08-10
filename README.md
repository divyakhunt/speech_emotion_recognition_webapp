# Speech Emotion Recognition Web App 🎙️😊😢😡

This is a **Speech Emotion Recognition** web application that detects emotions from speech input.  
It can classify audio into the following emotions:  
**Happy, Sad, Fear, Angry, Disgust, Surprise, Neutral**.

The app is built using **Python**, **Gradio**, and a trained deep learning model, and is deployed on **Hugging Face Spaces**.

---

## 🚀 Live Demo
Try the live app here:  
👉 [Speech Emotion Recognition on Hugging Face](https://huggingface.co/spaces/divyakhunt/speech-emotion-recognition)

---

## 📂 Project Structure

```
├── app.py                      # Main app file to run the Gradio interface
├── encoder.pkl                  # Label encoder for mapping classes
├── inference.py                 # Script for loading model and making predictions
├── README.md                    # Project documentation
├── requirements.txt             # Python dependencies
├── scaler.pkl                   # Scaler for feature normalization
├── speech_emotion_model.keras   # Trained speech emotion recognition model
├── utils.py                     # Utility functions for audio processing
```

---

## 📊 Model Training
The deep learning model was trained using a dataset of labeled speech samples.  
If you want to see the **model training process** and explore the `.ipynb` notebook, visit:  
[Model Training Repository](https://github.com/divyakhunt/speech_emotion_recognition)

---

## ⚙️ Installation & Usage

1. **Clone the repository**
```bash
git clone https://github.com/divyakhunt/speech_emotion_recognition_webapp.git
cd speech_emotion_recognition_webapp
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run locally**
```bash
python app.py
```
This will start a local Gradio server.  
Open the displayed URL in your browser to interact with the app.

---

## 📦 Features

- 🎤 **Record or upload** your voice
- 🧠 **Deep learning model** trained to recognize multiple emotions
- ⚡ **Real-time prediction** using Gradio interface
- 🌐 **Hosted on Hugging Face Spaces**

---

## 🎯 Supported Emotions
- 😀 Happy  
- 😢 Sad  
- 😨 Fear  
- 😡 Angry  
- 🤢 Disgust  
- 😲 Surprise  
- 😐 Neutral  

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements
- [Gradio](https://www.gradio.app/) for building quick ML web interfaces
- [Hugging Face Spaces](https://huggingface.co/spaces) for free model hosting
