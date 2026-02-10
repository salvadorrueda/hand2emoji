# hand2emoji 🖐️➡️😊

**hand2emoji** is a real-time computer vision application that detects hand gestures and overlays corresponding emojis on your webcam feed.

## Features
- **Real-time Hand Detection**: Uses MediaPipe for fast and accurate hand tracking.
- **Gesture Recognition**: Identifies gestures like Open Hand, Fist, Victory, Thumbs Up, and Pointing.
- **Emoji Overlay**: Displays a fun emoji (e.g., 🖐️, ✊, ✌️) following your hand.

## Installation

1. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```bash
python3 main.py
```

- **Press 'q'** to quit the application.

## Supported Gestures
| Gesture | Emoji |
| :--- | :---: |
| Open Hand | 🖐️ |
| Fist | ✊ |
| Victory | ✌️ |
| Thumbs Up | 👍 |
| Pointing | ☝️ |
