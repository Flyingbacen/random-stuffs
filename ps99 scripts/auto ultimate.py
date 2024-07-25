from pydirectinput import press
from pyautogui import pixelMatchesColor
from time import sleep as pause
from win32gui import GetWindowText as WindowTitle, GetForegroundWindow as ForegroundWindow

while True: 
    if "Roblox" in WindowTitle(ForegroundWindow()):
        if pixelMatchesColor(541, 892, (112, 237, 252), 5) or pixelMatchesColor(574, 977, (112, 237, 252), 5) or 1 == 2:
            press("r")
        else:
            pause(10)