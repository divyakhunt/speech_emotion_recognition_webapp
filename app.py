import gradio as gr
import time
from inference import predict_emotion # Assuming 'inference.py' with 'predict_emotion' exists

# --- 1. Configuration ---
# Central dictionary mapping emotions to their UI representation (emoji and color).
# This makes it easy to add or modify emotions in one place.
EMOTION_MAP = {
    "happy":     {"emoji": "😊", "color": "#FBBF24"},  # Warm, joyful gold/yellow
    "sad":       {"emoji": "😢", "color": "#60A5FA"},  # Softer, classic blue
    "fear":      {"emoji": "😨", "color": "#A78BFA"},  # Muted, anxious lavender/purple
    "angry":     {"emoji": "😠", "color": "#EF4444"},  # Vibrant, fiery red
    "disgust":   {"emoji": "🤢", "color": "#10B981"},  # Murky, earthy green/teal
    "surprised": {"emoji": "😲", "color": "#F472B6"},  # Bright, popping pink
    "neutral":   {"emoji": "😐", "color": "#9CA3AF"},  # Standard, balanced gray
    "not_found": {"emoji": "🤷‍♂️", "color": "#6B7280"}  # Darker, secondary gray for errors
}

# --- 2. UI Helper Functions ---
# These functions generate HTML content for different states of the output panel.

def get_placeholder_html():
    """Returns the initial HTML content for the result panel."""
    return """
    <div class="result-container placeholder">
        <div class="result-emoji">🎤</div>
        <div class="result-text">Emotion will appear here</div>
    </div>
    """

def get_processing_html():
    """Returns the HTML content shown while the model is analyzing the audio."""
    return """
    <div class="result-container processing">
        <div class="loading-spinner"></div>
        <div class="result-text">Analyzing your voice...</div>
    </div>
    """

def create_result_html(emotion: str):
    """
    Generates the final HTML to display the detected emotion.
    
    Args:
        emotion (str): The predicted emotion string (e.g., "happy").
    
    Returns:
        str: A formatted HTML string for the result display.
    """
    details = EMOTION_MAP.get(emotion, EMOTION_MAP["not_found"])
    emoji = details["emoji"]
    color = details["color"]
    
    # Convert hex color to RGB for use in CSS variables (for transparent gradients)
    rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    return f"""
    <div class="result-container predicted" style="--emotion-color: {color}; --emotion-color-rgb: {rgb[0]},{rgb[1]},{rgb[2]};">
        <div class="result-title">EMOTION DETECTED</div>
        <div class="result-emoji">{emoji}</div>
        <div class="result-text">{emotion.capitalize()}</div>
    </div>
    """

# --- 3. Core Logic & Event Handlers ---
# These functions are triggered by user interactions in the Gradio interface.

def classify_emotion(audio_file_path: str):
    """
    Main function called on "Submit". It handles the entire prediction process.
    It yields intermediate HTML updates for a better user experience.
    
    Args:
        audio_file_path (str): The file path to the user's audio recording.
    
    Yields:
        str: HTML strings to update the output component.
    """
    if audio_file_path is None:
        gr.Warning("Please record or upload an audio file first!")
        return get_placeholder_html()

    # 1. Show processing state
    yield get_processing_html()
    
    # 2. Simulate model processing time and get prediction
    time.sleep(2)  # Placeholder for actual model inference time
    emotion = predict_emotion(audio_file_path).lower()
    
    # 3. Show final result
    yield create_result_html(emotion)

def clear_all():
    """
    Resets the UI to its initial state when the "Clear" button is clicked.
    
    Returns:
        tuple: A tuple containing the new values for the UI components to be cleared.
    """
    return None, get_placeholder_html()


# --- 4. CSS Styling ---
# Custom CSS to give the application a modern and polished look.
APP_CSS = """
/* --- Google Fonts & CSS Variables --- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
:root {
    --primary-color: #2563EB;           /* Deep blue */
    --primary-hover: #1D4ED8;
    --text-color-main: #D1D5DB;         /* Slightly dimmed white */
    --text-color-subtle: #6B7280;       /* Muted gray */
    --bg-color-main: #0B0F19;           /* Near black background */
    --bg-color-panel: #111827;          /* Slightly lighter than bg */
    --border-color: #1F2937;            /* Dark border */
    --shadow-color: rgba(0, 0, 0, 0.2);  /* Softer, darker shadows */
    --font-family: 'Inter', sans-serif;
}


/* --- General & App Layout --- */
body { background: var(--bg-color-main); font-family: var(--font-family); color: var(--text-color-main); }
.gradio-container { 
    background: var(--bg-color-main); 
    border: none !important; 
    padding: 2rem; 
    /* Add these 3 lines for a full-height layout */
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Add this new rule to push the footer down */
.footer {
    margin-top: auto;
    padding-top: 2rem; 
    text-align: center;
}

#main-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.75rem;
    color: #FFFFFF;
}

#description {
    text-align: center;
    max-width: 700px;
    margin: 0 auto 2.5rem auto;
    font-size: 1.1rem;
    color: var(--text-color-subtle);
    line-height: 1.6;
}

/* --- Columns, Panels, and Buttons --- */
#app-columns { 
    gap: 2.5rem; 
    flex-grow: 1; /* Add this line to make content expand */
}

.panel {
    background: var(--bg-color-panel);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 2rem !important;
    height: 100%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.panel-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    text-align: center;
    color: var(--text-color-main);
}

#button-row {   
    gap: 0.75rem;
}

.gradio-button {
    background: var(--bg-color-panel) !important;
    color: var(--text-color-main) !important;
    border-radius: 8px !important;
    border: 1px solid var(--border-color) !important;
    font-weight: 600 !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: none !important;
}
.gradio-button:hover {
    border-color: var(--primary-color) !important;
    color: var(--primary-color) !important;
    transform: translateY(-1px);
}
#submit_btn {
    background: var(--primary-color) !important;
    color: #FFFFFF !important;
    border-color: var(--primary-color) !important;
}
#submit_btn:hover {
    background: var(--primary-hover) !important;
    border-color: var(--primary-hover) !important;
    color: #FFFFFF !important;
}

/* --- Input Panel (Left) --- */
#input-column .gradio-audio > div:first-of-type {
    background: #111827;
    border-radius: 12px;
    border: 1px solid var(--border-color);
}
#input-column audio { width: 100%; }
#input-column .label-wrap { display: none !important; }

/* --- Output Panel (Right) & Result Display --- */
.result-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    padding: 2rem;
    border-radius: 12px;
    transition: all 0.4s ease;
}
.result-container.placeholder {
    background: transparent;
    border: 2px dashed var(--border-color);
}
.placeholder .result-emoji { font-size: 4rem; animation: none; }
.placeholder .result-text { color: var(--text-color-subtle); }
.result-container.processing {
    background: transparent;
    border: 2px dashed var(--primary-color);
}
.result-container.predicted {
    background: linear-gradient(145deg, rgba(var(--emotion-color-rgb), 0.1), rgba(var(--emotion-color-rgb), 0.05));
    border: 1px solid var(--emotion-color);
    animation: popIn 0.5s ease-out;
}
.result-title {
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--text-color-subtle);
    margin-bottom: 1rem;
}
.result-emoji {
    font-size: 5rem;
    line-height: 1;
    margin-bottom: 1.5rem;
    margin-top: 1.3rem;
    animation: bounce 2.5s infinite ease-in-out;
}
.result-text {
    font-size: 1.75rem;
    font-weight: 600;
    color: #FFFFFF;
}

/* --- Animations & Spinners --- */
.loading-spinner {
    width: 50px;
    height: 50px;
    border: 4px solid #374151;
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1.5rem;
}
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes popIn { from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; } }
@keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }

/* --- Responsive Design --- */
@media (max-width: 768px) {
    .gradio-container { padding: 1rem; }
    #main-title { font-size: 2.25rem; }
    #description { font-size: 1rem; }
    #app-columns { flex-direction: column; gap: 1.5rem; }
    .panel { padding: 1.5rem !important; }
}

"""

# --- 5. Gradio Interface Definition ---
# The `with gr.Blocks()` context manager is used to build the custom UI.
with gr.Blocks(css=APP_CSS, theme="soft") as iface:
    # Header
    gr.HTML('<h1 id="main-title">🗣️ Speech Emotion Recognition</h1>')
    gr.HTML('<p id="description">Record your voice or upload an audio file, then hit Submit. Our AI will analyze the emotional tone. Use Clear to reset.</p>')
    
    # Main content area with two columns
    with gr.Row(elem_id="app-columns"):
        # Left Column: Input
        with gr.Column(elem_id="input-column", scale=1):
            with gr.Blocks(elem_classes="panel"):
                gr.HTML('<h2 class="panel-title">Your Voice Input</h2>')
                audio_input = gr.Audio(type="filepath", label="Record or Upload")
                with gr.Row(elem_id="button-row"):
                    clear_btn = gr.Button("Clear")
                    submit_btn = gr.Button("Submit", elem_id="submit_btn")
        
        # Right Column: Output
        with gr.Column(elem_id="output-column", scale=1):
            with gr.Blocks(elem_classes="panel"):
                gr.HTML('<h2 class="panel-title">Detected Emotion</h2>')
                html_output = gr.HTML(value=get_placeholder_html())
    
    # --- Event Listeners ---
    # Connect the buttons to their respective handler functions.
    submit_btn.click(
        fn=classify_emotion,
        inputs=audio_input,
        outputs=html_output,
        show_progress="hidden"
    )
    
    clear_btn.click(
        fn=clear_all,
        inputs=None,
        outputs=[audio_input, html_output],
        show_progress="hidden"
    )

# --- 6. Application Entry Point ---
# The standard Python idiom to run the script's main functionality.
if __name__ == "__main__":
    iface.launch()
