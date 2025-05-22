from dispatcher import handle_command
from speech import listen, speak
import keyboard

HOTKEY = "ctrl+shift+m"

def main():
    print(f"[MAVIS] Ready! Press {HOTKEY} or type a command.")
    
    keyboard.add_hotkey(HOTKEY, run_voice_command)

    while True:
        cmd = input(">> ").strip()
        if cmd:
            handle_command(cmd)

def run_voice_command():
    print("[MAVIS] Listening...")
    text = listen()
    if text:
        print(f"You said: {text}")
        handle_command(text)

if __name__ == "__main__":
    main()
