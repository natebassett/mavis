from commands.tell_time import run as tell_time
from speech import speak

def handle_command(cmd):
    cmd = cmd.lower()

    if "time" in cmd:
        tell_time()
    else:
        speak("Sorry, I didn't understand that.")
