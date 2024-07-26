from pyautogui import pixelMatchesColor as MatchesColor, locateOnScreen as FindImage, screenshot, ImageNotFoundException
import pydirectinput as input
import time
import random
import numpy as np



# Teleport settings
TPWAITTIME = 5
TELEPORTBUTTON = (168, 373)
TELEPORTBUTTONCOLOR = (133, 171, 190)
AREA1 = (548, 345)
AREA3 = (964, 345)
WORLD1 = (410, 449)
WORLD2 = (WORLD1[0], WORLD1[1] + 65)
WORLD3 = (WORLD1[0], WORLD1[1] + 130)
WORLDTPWAITTIME = 10
WORLDTPCONFIRM = (794, 718)

# Wheel settings
IMAGESPATH = ".\\..\\..\\Pictures\\"
SPINNYWHEELSPIN = (650, 707)
SPINNYWHEELX = (1469, 260)
SPINNYWHEELOK = (958, 720)

# OCR settings
n=time.time()
import easyocr # comment if you're seting useocr to False
# NOTE: All images are not given, and only regular huges are detected. This is theoretically more reliable than image detection
USEOCR = True
USEOCRMOUSEPOS = (1123, 333)
OCRREGION = (1143, 346, 259, 41)
if USEOCR:
    reader = easyocr.Reader(['en'])
    print("Time to load OCR: " + str(round(time.time()-n, 2)))


def jitterclick(x:int, y:int, num:int=2, click:bool=True): # stolen from my auto fuse macro
    """jitter the mouse so that the game recognizes the mouse is over the item"""
    something = 0
    while something <= num: # jitter num times
        input.moveTo(random.randint(x+1, x+5), random.randint(y, y+5))
        something += 1
    input.moveTo(x, y)
    if click:
        input.click(x, y)

def main(useocr:bool):
    def wheelsearch(huge:int):
        if huge == 1:   name = "Huge Propeller Cat"
        elif huge == 2: name = "Huge Abyssal Axolotl"
        elif huge == 3: name = "Huge Atomic Axolotl"

        while True:
            if not useocr:
                try:
                    if FindImage(IMAGESPATH + f"huge{huge}.png", confidence=0.9):
                        print(name + " found!")
                        jitterclick(*SPINNYWHEELSPIN) # spin the wheel
                        jitterclick(*SPINNYWHEELX) # press the X
                        time.sleep(0.5)
                        jitterclick(*SPINNYWHEELOK) # press the OK
                        time.sleep(1)
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
            if useocr:
                jitterclick(1123, 333, 1, False)
                file = np.array(screenshot(region = OCRREGION))
                result = reader.readtext(file) 
                example_result = [([[20, 4], [160, 4], [160, 32], [20, 32]], 'Mini Chest', 0.7377096682614568)]
                if result:
                    if result[0][1] == name:
                        print(name + " found")
                        jitterclick(*SPINNYWHEELSPIN) # spin the wheel
                        jitterclick(*SPINNYWHEELX) # press the X
                        time.sleep(0.5)
                        jitterclick(*SPINNYWHEELOK) # press the OK
                        time.sleep(1)
                    else:
                        print(f"---\nfound {result[0][1]}\n{name} not found\n---")
                        break
                else:
                    print("failed to read the image")
                    break
    def world1():
        while True:
            if MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                # TP area 3
                jitterclick(*TELEPORTBUTTON)
                time.sleep(0.5)
                jitterclick(*AREA3) 
                time.sleep(TPWAITTIME)

                input.press('q')
                # Entering area 3
                input.keyDown('w') 
                time.sleep(0.5)
                input.keyUp('w')

                # Entering Castle
                input.keyDown('a') 
                time.sleep(1.9)
                input.keyUp('a')

                # Go to the wheel 
                input.keyDown('s')
                time.sleep(1)
                input.keyUp('s')
                break
            else:
                time.sleep(1)
                
        # Spin the wheel if huge
        wheelsearch(1)
        
        # leave the wheel menu
        input.keyDown('w')
        time.sleep(0.5)
        input.keyUp('w')
        jitterclick(*SPINNYWHEELX)

        # Teleport to World 2
        jitterclick(*TELEPORTBUTTON)
        time.sleep(0.5)
        jitterclick(*WORLD2)
        time.sleep(0.5)
        jitterclick(*WORLDTPCONFIRM)
        time.sleep(WORLDTPWAITTIME)
    def world2():
        while True:
            # TP to area 102 and back for regular positioning
            if MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                jitterclick(*TELEPORTBUTTON)
                time.sleep(0.5)
                jitterclick(*AREA3)
                time.sleep(TPWAITTIME)
                jitterclick(*TELEPORTBUTTON)
                time.sleep(0.5)
                jitterclick(*AREA1)
                time.sleep(TPWAITTIME)

                # Go to spinny wheel
                input.press('q')
                input.keyDown('w')
                time.sleep(0.8)
                input.keyUp('w')
                input.keyDown('a')
                time.sleep(2.35)
                input.keyUp('a')
                input.keyDown('w')
                time.sleep(0.2)
                input.press('space')
                time.sleep(0.6)
                input.keyUp('w')
                break
            else:
                time.sleep(1)

        # Spin the wheel if huge
        wheelsearch(2)
        
        # leave the wheel menu
        input.keyDown('s')
        time.sleep(0.5)
        input.keyUp('s')
        jitterclick(*SPINNYWHEELX)

        # TP to world 3
        jitterclick(*TELEPORTBUTTON)
        time.sleep(0.5)
        jitterclick(*WORLD3)
        time.sleep(0.5)
        jitterclick(*WORLDTPCONFIRM)
        time.sleep(WORLDTPWAITTIME)
    def world3():
        while True:
            # TP to area 200 and back for regular positioning
            if MatchesColor(*TELEPORTBUTTON, TELEPORTBUTTONCOLOR, 3):
                jitterclick(*TELEPORTBUTTON)
                time.sleep(0.5)
                jitterclick(*AREA1)
                time.sleep(TPWAITTIME)
                jitterclick(*TELEPORTBUTTON)
                time.sleep(0.5)
                jitterclick(*WORLD3)
                time.sleep(TPWAITTIME)
                break
            else:
                time.sleep(1)

        # Go to spinny wheel
        input.press('q')
        input.keyDown('d')
        time.sleep(0.4)
        input.keyUp('d')
        input.keyDown('s')
        time.sleep(1.5)
        input.keyUp('s')

        # Spin the wheel if huge
        wheelsearch(3)

        # leave the wheel menu
        input.keyDown('w')
        time.sleep(0.5)
        input.keyUp('w')
        jitterclick(*SPINNYWHEELX)

        # TP to world 1
        jitterclick(*TELEPORTBUTTON)
        time.sleep(0.5)
        jitterclick(*WORLD1)
        time.sleep(0.5)
        jitterclick(*WORLDTPCONFIRM)
        time.sleep(WORLDTPWAITTIME)


    while True:
        world1()
        world2()
        world3()



if __name__ == '__main__':
    try:
        main(USEOCR)
    except KeyboardInterrupt:
        print("exiting")
    except input.FailSafeException:
        print("move your mouse")
        while True:
            try:
                input.keyUp('w')
                input.keyUp('a')
                input.keyUp('s')
                input.keyUp('d')
                exit()
            except input.FailSafeException:
                pass