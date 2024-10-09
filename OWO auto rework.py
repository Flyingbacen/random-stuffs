import pyautogui
import threading
from keyboard import add_hotkey, remove_hotkey, wait

def hunt():
    global running
    pyautogui.sleep(0.5)
    while running:
        pyautogui.typewrite("owo hunt  ")
        pyautogui.press("enter")
        pyautogui.sleep(15)
def battle():
    global running
    while running:
        pyautogui.typewrite("owo battle")
        pyautogui.press("enter")
        pyautogui.sleep(15)
def stop():
    global running
    running = False
    hunt.join()
    battle.join()

hunt = threading.Thread(target=hunt)
battle = threading.Thread(target=battle)

if __name__ == "__main__":
    add_hotkey("s", lambda: [hunt.start(), battle.start(), remove_hotkey("s"), add_hotkey("q", stop)])
    wait()