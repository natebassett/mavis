from datetime import datetime
from speech import speak

def run():
    now = datetime.now().strftime("%H:%M")
    speak(f"The time is {now}")
