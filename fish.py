from pyautogui import sleep, click, pixelMatchesColor
def tapfish(delay):
    while True:
        if pixelMatchesColor(1490, 224, (152,252,100), 10):
            sleep(1)
            click()
            sleep(4)
        else:
            click()
            sleep(delay)
choice = input("please input delay between clicks (in tenths of a second): ")
tapfish(float("0." + choice))
