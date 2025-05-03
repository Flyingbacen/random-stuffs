import pydirectinput
import keyboard

IsMouseDown = False

def togglemouse():
    global IsMouseDown

    if IsMouseDown:
        pydirectinput.mouseUp()
        IsMouseDown = False
    else:
        pydirectinput.mouseDown()
        IsMouseDown = True

keyboard.add_hotkey('f', togglemouse)
print("Press 'f' to toggle mouse click lock")
keyboard.wait()