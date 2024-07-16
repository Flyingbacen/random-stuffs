import pydirectinput
import pyautogui
import time

def main():
    ecoords = 800, 510
    okcoords = 690, 725
    ecolor = (255, 255, 255)
    okcolor = (125, 245, 13)
    try:
        while True:
            if pyautogui.pixelMatchesColor(*ecoords, ecolor, tolerance=10):
                pydirectinput.press("e")
                time.sleep(0.3)
                if pyautogui.pixelMatchesColor(*okcoords, okcolor, tolerance=10):
                    pydirectinput.click(*okcoords, 10, 0.1)
                    time.sleep(4)
                else:
                    print(str(pyautogui.pixel(*okcoords)))
            time.sleep(0.5)
    except pydirectinput.FailSafeException:
        print("Program ended")
        return

if __name__ == "__main__":
    time.sleep(5)
    main()