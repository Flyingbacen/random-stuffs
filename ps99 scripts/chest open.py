import pydirectinput
import pyautogui
import time

def main():
    ecoords = (0, 0) # 800, 510 # set to (0, 0) to ignore the button check
    okcoords = 690, 725
    ecolor = (255, 255, 255)
    okcolor = (125, 245, 13)
    try:
        while True:
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

if __name__ == "__main__":
    time.sleep(2) # 5 seconds to switch to the game
    main()