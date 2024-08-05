import io
import win32clipboard
from PIL import ImageGrab
import keyboard
from translate import Translator
import numpy as np
import os
import pyautogui
from win32gui import GetWindowText as WindowTitle, GetForegroundWindow as ForegroundWindow

TRANSLATE = True
IMAGE_TO_CLIPBOARD = False
DEFAULTREGION = 567, 671, 1351, 827
REGION = DEFAULTREGION

if not TRANSLATE and not IMAGE_TO_CLIPBOARD:
    print('No action selected, please set TRANSLATE and/or IMAGE_TO_CLIPBOARD to True')
    exit()

if TRANSLATE:
    print('loading easyocr...')
    import easyocr
    reader = easyocr.Reader(['ch_sim', 'en'])
    translator = Translator(to_lang='en', from_lang='zh-Hans')
    print('easyocr loaded')

os.system('cls')
print("activate the window you want to translate/screenshot and press /")
keyboard.wait('/', suppress=True)
WINDOW_NAME = WindowTitle(ForegroundWindow())

def take_screenshot():
    if WINDOW_NAME != WindowTitle(ForegroundWindow()):
        return
    global REGION
    rresult = ''
    screenshot = ImageGrab.grab(bbox=REGION)
    if TRANSLATE: np_screenshot = np.array(screenshot)
    if TRANSLATE:
        easyocr_result = reader.readtext(np_screenshot)
        # print(easyocr_result) # Debug
        print('---\nDetected text\n')
        for result in easyocr_result:
            print(result[1])
            rresult += result[1]

        print('---\nTranslated text\n')
        print(translator.translate(rresult))
        # for result in easyocr_result: # old version, slower and depending on the sentence structure made less sense
        #     print(translator.translate(result[1]))

    if IMAGE_TO_CLIPBOARD:
        output = io.BytesIO()
        screenshot.save(output, format='BMP')
        bmp_data = output.getvalue()[14:]

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
        win32clipboard.CloseClipboard()
def change_region(default=False):
    global REGION
    if WINDOW_NAME != WindowTitle(ForegroundWindow()):
        return
    if default:
        REGION = DEFAULTREGION
        print(f'Region set to {REGION}')
        return
    print('Press enter to set top left corner')
    keyboard.wait('enter', suppress=True)
    top_left = pyautogui.position()
    print('Press enter to set bottom right corner')
    keyboard.wait('enter', suppress=True)
    bottom_right = pyautogui.position()
    REGION = (top_left.x, top_left.y, bottom_right.x, bottom_right.y)
    print(f'Region set to {REGION}')

def cls():
    if WINDOW_NAME != WindowTitle(ForegroundWindow()):
        return
    os.system('cls')


print(f'Window name: {WINDOW_NAME}')
print("s: screenshot/translate\nd: clear screen\nshift+[: set region\nshift+r: reset region to default\n")
keyboard.add_hotkey('s', take_screenshot)
keyboard.add_hotkey('d', cls)
keyboard.add_hotkey('shift+[', change_region)
keyboard.add_hotkey('shift+r', change_region, args=[True])
keyboard.wait()
