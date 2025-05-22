from memory import recall
from speech import speak

def run(cmd):
    try:
        if "what is" in cmd:
            key = cmd.lower().split("what is", 1)[1].strip()
        elif "what's" in cmd:
            key = cmd.lower().split("what's", 1)[1].strip()
        else:
            key = cmd.strip()

        value = recall(key)
        if value:
            speak(f"{key} is {value}")
        else:
            speak(f"I don't know what {key} is.")
    except Exception as e:
        speak("Sorry, I couldn't recall that.")
        print(f"[Recall Error] {e}")
