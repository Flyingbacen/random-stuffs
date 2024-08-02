import pydirectinput
import pyautogui
import time
import threading
import keyboard

def main():
    ecoords = (0, 0) # 800, 510 # set to (0, 0) to ignore the button check
    okcoords = 690, 725
    ecolor = (255, 255, 255)
    okcolor = (125, 245, 13)
    global running
    running = True
    try:
        while running:
            if pyautogui.pixelMatchesColor(*ecoords, ecolor, tolerance=10) or ecoords == (0, 0):
                pydirectinput.press("e")
                time.sleep(0.3)
                while True:
                    if pyautogui.pixelMatchesColor(*okcoords, okcolor, tolerance=10):
                        pydirectinput.click(*okcoords, 10, 0.1)
                        time.sleep(4)
                        break
                    else:
                        break
            time.sleep(0.1)
    except pydirectinput.FailSafeException:
        print("Program ended")
        return

def stop():
    global running
    running = False
    main_thread.join()
    print("Exited")
    exit()

if __name__ == "__main__":
    main_thread = threading.Thread(target=main)
    print("Press F3 to start, F8 to stop")
    keyboard.add_hotkey("f3", lambda: (main_thread.start(), keyboard.add_hotkey("f8", stop)))
    keyboard.wait("f8")