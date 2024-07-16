from pyautogui import sleep, click, pixelMatchesColor
def tapfish(delay: float, fish):
    while True:
        if pixelMatchesColor(1490, 224, (152,252,100), 10):
            fish += 1
            print(f"Caught fish #{fish}")
            sleep(1)
            click()
            sleep(4) # If the fishing rod is pulling too early, increase this number
        else:
            click()
            sleep(delay)
tapfish(float(input("input delay in seconds between clicks (0.1 works fine): ")), 0)
