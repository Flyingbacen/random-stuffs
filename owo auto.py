from pyautogui import typewrite as owotype
from time import sleep as owosleep
import threading as owothreading

def begin(wait: int = 2):
    """
    Move your mouse to any corner for about 15 seconds to stop the script (pyautogui feature).
    Alternatively, close the window. Ctrl+C doesn't work because making the threads daemnon breaks it 🤷‍♀️.
    parameters:
    wait (int): Set to 2 as default, used to ensure you're in the correct window first before starting threads.
    returns:
    None
    """
    
    if wait > 0:
        owosleep(wait)
    def timer_owohunt():
        while True:
            print("Typing 'owo hunt'")
            owotype("owo hunt\n")
            owosleep(15)

    def timer_owobattle():
        while True:
            print("Typing 'owo battle'")
            owotype("owo battle\n")
            owosleep(16)
    
    thread_owohunt = owothreading.Thread(target=timer_owohunt)
    thread_owobattle = owothreading.Thread(target=timer_owobattle)
    thread_owohunt.start()
    owosleep(0.3)           # Ensures the messages won't interfere with each other (hopefully)
    thread_owobattle.start()

begin()