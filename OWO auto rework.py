import asyncio
import pyautogui

async def hunt():
    await asyncio.sleep(0.5)
    while True:
        pyautogui.typewrite("owo hunt")
        pyautogui.press("enter")
        await asyncio.sleep(15.2)
async def battle():
    while True:
        pyautogui.typewrite("owo battle")
        pyautogui.press("enter")
        await asyncio.sleep(15.2)

async def main():
    hunting = asyncio.create_task(hunt())
    battleing = asyncio.create_task(battle())
    await hunting
    await battleing

if __name__ == "__main__":
    pyautogui.sleep(2)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting")
        exit()