# MedAssistant

**MedAssistant** is a voice-based medical assistant that can remind you to take your medication, tell the current time, and respond to voice commands.  
It uses **Python, Tkinter, SpeechRecognition, pyttsx3, and Docker**.

## Features

- Simple GUI with Tkinter  
- Medication reminders based on schedule  
- Voice commands: medicine, add medicine, time, doctor  
- Dockerized for easy deployment  

## Installation and Usage

### 1. Run with Python

1. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install python3-tk portaudio19-dev espeak ffmpeg libespeak1

Run the program:

python med.py

2. Run with Docker

Build Docker image:

docker build -t medassistant:latest .


Run the container with GUI support:

docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix medassistant:latest


Run the container in voice-only mode:

docker run -it --rm medassistant:latest