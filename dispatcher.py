from commands.tell_time import run as tell_time
from commands.remember import run as remember
from commands.recall import run as recall
from speech import speak

def handle_command(cmd):
    cmd = cmd.lower()

    if "time" in cmd:
        tell_time()
    elif "remember" in cmd:
        remember(cmd)
    elif "what is" in cmd or "what's" in cmd:
        recall(cmd)
    else:
        speak("Sorry, I didn't understand that.")
