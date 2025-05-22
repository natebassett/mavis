import pyttsx3
import sounddevice as sd
import queue
import vosk
import json
import os

# Set model path
model_path = "models/vosk-model-small-en-us-0.15"

# Load Vosk model
if not os.path.exists(model_path):
    raise FileNotFoundError("Vosk model not found. Download and place it in /models.")

model = vosk.Model(model_path)
q = queue.Queue()
tts = pyttsx3.init()

def speak(text):
    tts.say(text)
    tts.runAndWait()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")
