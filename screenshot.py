import io
import win32clipboard
from PIL import ImageGrab
import keyboard
from translate import Translator
import numpy as np
import os
import pyautogui
import json
from win32gui import GetWindowText as WindowTitle, GetForegroundWindow as ForegroundWindow

global translatedStrings
translatedStrings = []

if os.path.exists('config.json'):
    import json
    with open('./config.json') as f:
        config = json.load(f)
        TRANSLATE = config['translate']
        IMAGE_TO_CLIPBOARD = config['image_to_clipboard']
        DEFAULTREGION = tuple(config['region'])
else:
        
    TRANSLATE = True
    IMAGE_TO_CLIPBOARD = False
    DEFAULTREGION = 276, 790, 1646, 1056
    if input("Do you want to make a config file? (y/n): ").lower() == 'y':
        with open('.config.json', 'w') as f:
            config = {
                'translate': TRANSLATE,
                'image_to_clipboard': IMAGE_TO_CLIPBOARD,
                'region': list(DEFAULTREGION)
            }
            json.dump(config, f)
# DEFAULTREGION = 567, 671, 1351, 827
REGION = DEFAULTREGION

if not TRANSLATE and not IMAGE_TO_CLIPBOARD:
    print('No action selected, please set TRANSLATE and/or IMAGE_TO_CLIPBOARD to True')
    exit()

if TRANSLATE:
    print('loading easyocr...')
    import easyocr
    reader = easyocr.Reader(['en', 'ja'])
    translator = Translator(to_lang='en', from_lang='ja')
    print('easyocr loaded')

os.system('cls')
print("activate the window you want to translate/screenshot and press /")
keyboard.wait('/', suppress=True)
WINDOW_NAME = WindowTitle(ForegroundWindow())

def take_screenshot(ignorelist: bool = False):
    if WINDOW_NAME != WindowTitle(ForegroundWindow()):
        return
    global REGION
    screenshot = ImageGrab.grab(bbox=REGION)
    if IMAGE_TO_CLIPBOARD:
        output = io.BytesIO()
        screenshot.save(output, format='BMP')
        bmp_data = output.getvalue()[14:]

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
        win32clipboard.CloseClipboard()
    if TRANSLATE:
        np_screenshot = np.array(screenshot)
        easyocr_result = reader.readtext(np_screenshot, detail=0, paragraph=True, )
        try:
            if easyocr_result[0] in translatedStrings and not ignorelist:
                return
        except IndexError:
            print('No text detected')
            return
        
        print('---\nDetected text\n')
        for paragraph in easyocr_result:
            print(paragraph)

        translatedStrings.extend(easyocr_result)
        if len(translatedStrings) > 5:
            translatedStrings[:] = translatedStrings[-5:]
        if easyocr_result[0] == '':
            return
        if easyocr_result[0] == '': return

        print('---\nTranslated text\n')
        for paragraph in easyocr_result:
            print(translator.translate(paragraph))

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
print("s: screenshot/translate\nd: clear screen\n[: set region\nshift+r: reset region to default\n")
keyboard.add_hotkey('s', take_screenshot)
keyboard.add_hotkey('shift+s', take_screenshot, args=(True,))
keyboard.add_hotkey('d', cls)
keyboard.add_hotkey('[', change_region)
keyboard.add_hotkey('shift+r', change_region, args=(True,))
keyboard.wait()
