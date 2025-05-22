from memory import remember
from speech import speak

def run(cmd):
    try:
        # Extract key/value from "remember X is Y"
        parts = cmd.lower().split("remember", 1)[1].strip()
        if " is " in parts:
            key, value = parts.split(" is ", 1)
            remember(key.strip(), value.strip())
            speak(f"Got it. I'll remember {key.strip()} is {value.strip()}.")
        else:
            speak("Please say something like 'remember X is Y'.")
    except Exception as e:
        speak("Sorry, I couldn't remember that.")
        print(f"[Memory Error] {e}")
