import keyboard
import pydirectinput
import threading

running = True

def main():
    global running
    while running:
        pydirectinput.press("e")
        pydirectinput.leftClick(815, 697)

def stop():
    global running
    print("Exiting...")
    running = False

main_thread = threading.Thread(target=main)

keyboard.add_hotkey("f3", lambda: main_thread.start())
keyboard.add_hotkey("f8", stop)
keyboard.wait("f8")