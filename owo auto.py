from pyautogui import typewrite as owotype
from time import sleep as owosleep
import threading as owothreading
from queue import Queue as owoqueue

def begin(wait: int = 2):
    """
    parameters:
    wait (int): Set to 2 as default, used to ensure you're in the correct window first before starting threads.
    returns:
    None
    """
    ttt = owoqueue()
    ttt.put(0)
    try:
        if wait > 0:
            owosleep(wait)
        def timer_owohunt():
            while True:
                yyy = ttt.get()
                if yyy == 123:
                    print("Stopping hunt thread...")
                    return
                print("Typing 'owo hunt'")
                owotype("owo hunt\n")
                owosleep(15)

        def timer_owobattle():
            while True:
                yyy = ttt.get()
                if yyy==123:
                    print("Stopping battle thread...")
                    return
                print("Typing 'owo battle'")
                owotype("owo battle\n")
                owosleep(16)
        
    

        thread_owohunt = owothreading.Thread(target=timer_owohunt)
        thread_owobattle = owothreading.Thread(target=timer_owobattle)
        thread_owohunt.start()
        owosleep(0.3) # Ensures the messages won't interfere with each other (hopefully)
        thread_owobattle.start()
    except KeyboardInterrupt: # I can't get this thing to work, to the one person who's browsing github and comes to this repository and knows the solution, please give something 🙏
        print("Stopping threads...")
        ttt.put(123)
        thread_owohunt.join()
        thread_owobattle.join()



begin()

"""
owo hunt

"""
