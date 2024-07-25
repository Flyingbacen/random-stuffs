import pyautogui # check color of pixel, pydirectinput doesn't have it
import pydirectinput # Works identically to pyautogui, but works in DirectX games
import time
import random

def setup() -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int, int], bool, tuple[int, int], tuple[int, int], int, bool, tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
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
    achievement = True # enable if you just want the steampunk hoverboard (will take about 288 minutes (4.8 hours) with this script)
    timestats = False # enable if you want to see the time taken for each fuse, along with the average time
    return fuse_button, confirm_button, white_space_of_fuse_screen, green, achievement, page_forward_arrow, page_backward_arrow, close_after_fuse, timestats, pet1, pet2, pet3, pet4, pet5, pet6, pet7, pet8, pet9, pet10, pet11, pet12

def main(fuse_button:tuple[int, int], confirm_button:tuple[int, int], whitespace:tuple[int, int], green:tuple[int, int, int], achievement:bool, page_forward_arrow:tuple[int, int], page_backward_arrow:tuple[int, int], close_after_fuse:int, timestats:bool, pet1:tuple[int, int], pet2:tuple[int, int], pet3:tuple[int, int], pet4:tuple[int, int], pet5:tuple[int, int], pet6:tuple[int, int], pet7:tuple[int, int], pet8:tuple[int, int], pet9:tuple[int, int], pet10:tuple[int, int], pet11:tuple[int, int], pet12:tuple[int, int]):
    def jitter(x:int, y:int, num:int=2):
        """jitter the mouse so that the game recognizes the mouse is over the item"""
        something = 0
        while something <= num: # jitter num times
            pydirectinput.moveTo(random.randint(x, x+5), random.randint(y, y+5))
            something += 1

    def fuse():
        """check if the fuse button is green, if so, click it"""
        if pyautogui.pixelMatchesColor(*fuse_button, green, tolerance=10):
            jitter(*fuse_button)
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
    fused_pets = 0
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
                    if achievement: 
                        fused_pets += 1
                        print(f"Pet fused: {fused_pets}")
                    elif not achievement: 
                        fused_pets += num_pets * pages
                        print(f"Pets fused: {fused_pets}")
                    break
                else: time.sleep(0.1)
            if timestats:
                totaltime.append(time.time()-timestart)
                print(f"Time taken: {round(time.time()-timestart, 4)}")
                print(f"Current average time: {round(sum(totaltime)/len(totaltime), 4)}")
            fuse_count += 1
            if fuse_count == close_after_fuse:
                print("Program ended (close_after_fuse reached)")
                exit()

def destroy(reason:str):
    try:
        print(f"Program ended ({reason})")
        time.sleep(0.5)
        pydirectinput.keyUp("ctrl")
        print("ctrl key released")
    except pydirectinput.FailSafeException:
        print("Please move the mouse out of the corner after you trigger the exception so that cleanup can be done properly.")
        while True:
            try:
                pydirectinput.keyUp("ctrl")
                print("ctrl key released")
                break
            except pydirectinput.FailSafeException:
                pass
    finally:
        exit()

if __name__ == "__main__":
    print("To exit this script, you can\n1. Leave the fuse screen, go to the terminal and press ctrl+c\n2. shove your mouse into any corner of the screen")
    time.sleep(5) # 5 seconds to switch to the game
    try:
        main(*setup())
    except pydirectinput.FailSafeException:
        destroy("FailSafeException (expected)")
    except KeyboardInterrupt:
        destroy("KeyboardInterrupt (expected)")
    except Exception as e:
        print(f"An error occurred: {e}")
        destroy("Unhandled exception")