try:
    from pyautogui import pixelMatchesColor as MatchesColor, locateOnScreen as FindImage, screenshot, ImageNotFoundException
    import pydirectinput as input
    import time
    import random
    import numpy as np # Used to convert screenshot for OCR
    import keyboard # hotkey
except ImportError: # Install required modules if not found
    print("Installing required modules...")
    import os
    os.system("pip install pyautogui pydirectinput easyocr keyboard numpy torch torchvision torchaudio")
    print("Please restart the script.")

# region Settings
# region Misc. Initilization settings
HUGES_FOUND = [0, 0, 0]
input.PAUSE = 0.05
# endregion

# region Teleport settings
TELEPORTBUTTON = (168, 373)
TELEPORTBUTTONCOLOR = (133, 171, 190)
TELEPORTSCREEN = (650, 301)
TELEPORTSCREENCOLOR = (255, 255, 255)
CURRENTAREACOLOR = (116, 240, 251)
AREA1 = (548, 345)
AREA3 = (964, 345)
WORLD1 = (410, 449)
WORLD2 = (WORLD1[0], WORLD1[1] + 65)
WORLD3 = (WORLD1[0], WORLD1[1] + 130)
WORLDTPWAITTIME = 10 # Not too important, just make sure it's not too short
WORLDTPCONFIRM = (794, 718)
# endregion

# region Wheel settings
IMAGESPATH = "./../../Pictures/" # not used if OCR is enabled
SPINNYWHEELSPIN = (650, 707)
SPINNYWHEELX = (1469, 260)
SPINNYWHEELOKCOLOR = (127, 246, 14)
SPINNYWHEELOK = (864, 717)
SPINNYWHEELBLUECOLOR = (81, 223, 254)
SPINNYWHEELBLUE = (773, 441)
SPINNYWHEELWHITECOLOR = (255, 255, 255)
SPINNYWHEELWHITE = (868, 385)
EXTRA_WHEEL_OPTIONS = [ 
                      "example item",
                      "Chest Spell"
                      ] 
huge_names = {
             "world1": "Huge Propeller Cat", 
             "world2": "Huge Abyssal Axolotl", 
             "world3": "Huge Atomic Axolotl"
             }
# endregion

# region OCR settings
# NOTE: All images are not given, and only regular huges are detected. This is theoretically more reliable than image detection
n=time.time()
USEOCR = True
USEOCRMOUSEPOS = (1123, 333)
OCRREGION = (1143, 346, 259, 41)
if USEOCR:
    print("\nLoading OCR, please wait...")
    import easyocr
    reader = easyocr.Reader(['en'])
    print("Time to load OCR: " + str(round(time.time()-n, 2)) + "\n")
# endregion
# endregion


def jitterclick(x:int, y:int, num:int=2, click:bool=True): # stolen from my auto fuse macro
    """jitter the mouse so that the game recognizes the mouse is over the item"""
    something = 0
    while something <= num: # jitter num times
        input.moveTo(random.randint(x+1, x+5), random.randint(y, y+5))
        something += 1
    input.moveTo(x, y)
    if click:
        input.click(x, y)

def main(start_index:int, single_world:bool=False):
    def spin():
        jitterclick(*SPINNYWHEELSPIN)
        jitterclick(*SPINNYWHEELX)
        while True:
            if MatchesColor(*SPINNYWHEELOK, SPINNYWHEELOKCOLOR, 3):
                break
        jitterclick(*SPINNYWHEELOK)
    
    def wheelsearch(huge:int):
        name = huge_names.get(f"world{huge}", "error: unknown value")

        while True:
            while not MatchesColor(*SPINNYWHEELBLUE, SPINNYWHEELBLUECOLOR, 3) and MatchesColor(*SPINNYWHEELWHITE, SPINNYWHEELWHITECOLOR, 3):
                pass
            if not USEOCR:
                try:
                    if FindImage(IMAGESPATH + f"huge{huge}.png", confidence=0.9):
                        print(name + " found!")
                        spin()
                except ImageNotFoundException:
                    print(name + " not found")
                    break
                except OSError as e:
                    if "Failed to read" in str(e):
                        print("failed to read the image\nEnsure the images are in the correct folder")
                        break
                    else:
                        print(e)
                        break
            if USEOCR:
                jitterclick(1123, 333, 2, False)
                for i in EXTRA_WHEEL_OPTIONS:
                    EXTRA_WHEEL_OPTIONS[EXTRA_WHEEL_OPTIONS.index(i)] = i.lower()
                time.sleep(0.1)
                file = np.array(screenshot(region = OCRREGION))
                result = reader.readtext(file) 
                example_result = [([tuple, tuple, tuple, tuple], 'Mini Chest', float)]
                if result:
                    if result[0][1].lower() == name.lower() or "Huge" in result[0][1]:
                        print(name + " found")
                        HUGES_FOUND[huge-1] += 1
                        spin()
                    elif any([option in result[0][1].lower() for option in EXTRA_WHEEL_OPTIONS]):
                        print("\nExtra option found! spinning")
                        spin()
                    else:
                        print(f"found {result[0][1]}.\n{name} not found; leaving\n---")
                        break
                else:
                    print("failed to read the text")
                    break
            
    def move(key:str, length:float):
        input.keyDown(key)
        time.sleep(length)
        input.keyUp(key)


    def world1():
        while True:
            if MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                # TP area 3
                jitterclick(*TELEPORTBUTTON)
                while not MatchesColor(*TELEPORTSCREEN, TELEPORTSCREENCOLOR, 3):
                    pass
                jitterclick(*AREA3) 
                while MatchesColor(*TELEPORTSCREEN, TELEPORTSCREENCOLOR, 3): # Wait for the screen to close (lag)
                    pass
                jitterclick(*TELEPORTBUTTON)
                while not MatchesColor(*AREA3, CURRENTAREACOLOR, 3): #Watch to see what area you're in
                    pass
                jitterclick(*TELEPORTBUTTON)
                time.sleep(0.5)
                break

        # Go to the wheel 
        input.press('q')
        move('w', 0.75)
        move('a', 2.1)
        move('s', 1)
        # Spin the wheel if huge
        wheelsearch(1)
        # leave the wheel menu
        move('w', 0.5)
        jitterclick(*SPINNYWHEELX)
        # Teleport to World 2
        jitterclick(*TELEPORTBUTTON)
        while not MatchesColor(*TELEPORTSCREEN, TELEPORTSCREENCOLOR, 3):
            pass
        jitterclick(*WORLD2)
        time.sleep(0.5)
        jitterclick(*WORLDTPCONFIRM)
        time.sleep(WORLDTPWAITTIME)
    def world2():
        while True:
            # TP to area 102 and back for regular positioning
            if MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                jitterclick(*TELEPORTBUTTON)
                while not MatchesColor(*TELEPORTSCREEN, TELEPORTSCREENCOLOR, 3): # Wait for the screen to open
                    pass
                jitterclick(*AREA3)
                time.sleep(0.5)
                jitterclick(*TELEPORTBUTTON)
                while not MatchesColor(*AREA3, CURRENTAREACOLOR, 3):
                    pass
                time.sleep(0.5)
                while not MatchesColor(*TELEPORTSCREEN, TELEPORTSCREENCOLOR, 3):
                    pass
                jitterclick(*AREA1)
                time.sleep(0.5)
                jitterclick(*TELEPORTBUTTON)
                while not MatchesColor(*AREA1, CURRENTAREACOLOR, 3):
                    pass
                jitterclick(*TELEPORTBUTTON)
                time.sleep(0.5)
                break
        # Go to spinny wheel
        input.press('q')
        move('w', 0.8)
        move('a', 2.5)
        input.keyDown('w')
        time.sleep(0.2)
        input.press('space') # Jump onto the platform
        time.sleep(0.6)
        input.keyUp('w')
        wheelsearch(2)
        move('s', 0.5)
        jitterclick(*SPINNYWHEELX)
        jitterclick(*TELEPORTBUTTON)
        while not MatchesColor(*TELEPORTSCREEN, TELEPORTSCREENCOLOR, 3):
            pass
        jitterclick(*WORLD3)
        time.sleep(0.5)
        jitterclick(*WORLDTPCONFIRM)
        time.sleep(WORLDTPWAITTIME)
    def world3():
        while True:
            # TP to area 200 and back for regular positioning
            if MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                jitterclick(*TELEPORTBUTTON)
                while not MatchesColor(*TELEPORTSCREEN, TELEPORTSCREENCOLOR, 3):
                    pass
                jitterclick(*AREA1)
                while MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                    pass
                while not MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                    pass
                jitterclick(*TELEPORTBUTTON)
                while not MatchesColor(*TELEPORTSCREEN, TELEPORTSCREENCOLOR, 3):
                    pass
                jitterclick(*WORLD3) # Back to spawn
                while MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                    pass
                while not MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                    pass
                break

        input.press('q')
        move('d', 0.5)
        move('s', 1.5)
        wheelsearch(3)
        move('w', 0.5)
        jitterclick(*SPINNYWHEELX)
        jitterclick(*TELEPORTBUTTON)
        while not MatchesColor(*TELEPORTSCREEN, TELEPORTSCREENCOLOR, 3):
            pass
        jitterclick(*WORLD1)
        time.sleep(0.5)
        jitterclick(*WORLDTPCONFIRM)
        time.sleep(WORLDTPWAITTIME)

    worlds = [world1, world2, world3]
    if not single_world:
        while True:
            for i in range(start_index, start_index + len(worlds)): 
                worlds[i % len(worlds)]()
    else:
        this = 1
        if start_index == 0:
            backtoworld = WORLD1
        elif start_index == 1:
            backtoworld = WORLD2
        elif start_index == 2:
            backtoworld = WORLD3
        while True:
            if this == 1: # Do it once and never again
                worlds[start_index]()
                this += 1
            if MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                jitterclick(*TELEPORTBUTTON)
                while not MatchesColor(*TELEPORTSCREEN, TELEPORTSCREENCOLOR, 3):
                    pass
                jitterclick(*backtoworld)
                time.sleep(0.5)
                jitterclick(*WORLDTPCONFIRM)
                time.sleep(WORLDTPWAITTIME)
                worlds[start_index]()

def clean():
    # region cleanup
    while True:
        try:
            input.keyUp('w')
            input.keyUp('a')
            input.keyUp('s')
            input.keyUp('d')
            if HUGES_FOUND != [0, 0, 0]:
                print(f"""Huge Propeller Cat: {HUGES_FOUND[0]}
                    Huge Abyssal Axolotl: {HUGES_FOUND[1]}
                    Huge Atomic Axolotl: {HUGES_FOUND[2]}""")
            else: print("No huges found\n")
            print("Manually close the program")
            exit()
        except input.FailSafeException:
            pass
def shortcut(index, single_world=False):
    try:    
        keyboard.remove_all_hotkeys()
        main(index, single_world)
    except KeyboardInterrupt: print("exiting")
    except input.FailSafeException: print("move your mouse")
    except Exception as e: print(e)
    finally: clean()
# region hotkeys
print(
    """Press F1, F2, or F3, based on what world you're in to start from that world.
    use 1, 2, or 3 to use only that world. (this is overall slower, but useful if you don't have any of the other world's tickets)
    ---""")
keyboard.add_hotkey("f1", lambda: shortcut(0))
keyboard.add_hotkey("f2", lambda: shortcut(1))
keyboard.add_hotkey("f3", lambda: shortcut(2))
keyboard.add_hotkey("1", lambda: shortcut(0, True))
keyboard.add_hotkey("2", lambda: shortcut(1, True))
keyboard.add_hotkey("3", lambda: shortcut(2, True))
keyboard.wait()