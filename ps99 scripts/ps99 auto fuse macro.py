import pyautogui # check color of pixel, pydirectinput doesn't have it
import pydirectinput # Works more reliable in roblox than pyautogui
import sys # to exit the program
import time
import random

def setup():
    """
    setup the coordinates for the pets and buttons if the script does not work ootb
    - measure from the top-left corner of the screen
    """
    pet1 = 916, 390
    pet2 = 1063, 390
    pet3 = 1210, 390
    pet4 = 1368, 390
    pet5 = 916, 539
    pet6 = 1063, 539
    pet7 = 1210, 539
    pet8 = 1368, 539
    pet9 = 916, 700
    pet10 = 1063, 700
    pet11 = 1210, 700
    pet12 = 1368, 700
    page_forward_arrow = 1200, 790
    page_backward_arrow = 1105, 790
    fuse_button = 736, 710
    confirm_button = 1058, 716
    white_space_of_fuse_screen = 850, 280
    close_after_fuse = 0 # close the game after fusing x times, 0 to disable
    green = (129, 247, 14) # color of the green button, NOT coordinates. Most likely no need to change this
    achievement = True # enable if you just want the steampunk hoverboard (will take about 288 minutes with this script)
    timestats = False # enable if you want to see the time taken for each fuse, along with the average time
    return fuse_button, confirm_button, white_space_of_fuse_screen, green, achievement, page_forward_arrow, page_backward_arrow, close_after_fuse, timestats, pet1, pet2, pet3, pet4, pet5, pet6, pet7, pet8, pet9, pet10, pet11, pet12

def main(fuse_button:tuple[int, int], confirm_button:tuple[int, int], whitespace:tuple[int, int], green:tuple[int, int, int], achievement:bool, page_forward_arrow:tuple[int, int], page_backward_arrow:tuple[int, int], close_after_fuse:int, timestats:bool, pet1:tuple[int, int], pet2:tuple[int, int], pet3:tuple[int, int], pet4:tuple[int, int], pet5:tuple[int, int], pet6:tuple[int, int], pet7:tuple[int, int], pet8:tuple[int, int], pet9:tuple[int, int], pet10:tuple[int, int], pet11:tuple[int, int], pet12:tuple[int, int]):
    try:
        def jitter(x:int, y:int, num:int=1):
            """jitter the mouse so that the game recognizes the mouse is over the item"""
            something=0
            while something<=num: # jitter num times
                pydirectinput.moveTo(random.randint(x, x+5), random.randint(y, y+5))
                something+=1

        def fuse():
            """check if the fuse button is green, if so, click it"""
            if pyautogui.pixelMatchesColor(*fuse_button, green, tolerance=10):
                jitter(*fuse_button, 1)
                pydirectinput.leftClick(*fuse_button)
                return True
            else: return False

        def fuseconfirm():
            """click the confirm button when it appears"""
            if pyautogui.pixelMatchesColor(*confirm_button, green, tolerance=10):
                jitter(*confirm_button, 1)
                pydirectinput.leftClick(*confirm_button)
                return True
            else: return False

        fuse_count = 0
        if timestats: totaltime = []
        while True: # main loop
            if timestats: timestart = time.time()
            if pyautogui.pixelMatchesColor(*whitespace, (255, 255, 255), tolerance=10): # make sure you're in the fuse screen
                num_pets = 12 if not achievement else 3
                pages = 8 if not achievement else 1
                pets = [pet1, pet2, pet3, pet4, pet5, pet6, pet7, pet8, pet9, pet10, pet11, pet12]
                pydirectinput.keyDown("ctrl")
                def select_pets():
                    """selects all 12 pets on the screen"""
                    for i in range(num_pets):
                        jitter(*pets[i])
                        pydirectinput.leftClick(*pets[i])
                page_clicks = 0
                for _ in range(pages):
                    """for every page, select all pets"""
                    select_pets()
                    if not achievement:
                        jitter(*page_forward_arrow, 1)
                        pydirectinput.leftClick(*page_forward_arrow)
                        page_clicks += 1
                    time.sleep(0.1)
                for _ in range(page_clicks):
                    """go back to the page you started on"""
                    jitter(*page_backward_arrow, 1)
                    pydirectinput.leftClick(*page_backward_arrow)
                    
                pydirectinput.keyUp("ctrl")
                while True: # constantly check if the button is green
                    if fuse(): 
                        break
                while True: # constantly check for when the confirm button appears
                    if fuseconfirm():
                        break
                if timestats:
                    totaltime.append(time.time()-timestart)
                    print(f"Time taken: {round(time.time()-timestart, 2)}")
                    print(f"Current average time: {round(sum(totaltime)/len(totaltime))}")
                fuse_count += 1
                if fuse_count == close_after_fuse:
                    print("Program ended (close_after_fuse reached)")
                    sys.exit()
                    exit()
    except pydirectinput.FailSafeException: # shove your mouse in a corner to exit, added for pretty-print
        pydirectinput.keyUp("ctrl")
        print("Program ended (Failsafe exception)")
        sys.exit()
        exit() # sys.exit seems to only pause, so just in case
    except KeyboardInterrupt:
        pydirectinput.keyUp("ctrl")
        print(f"Program ended (Keyboard interrupt)")
        sys.exit()
        exit()

if __name__ == "__main__":
    time.sleep(5) # 5 seconds to switch to the game
    main(*setup())