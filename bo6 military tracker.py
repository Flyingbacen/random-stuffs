import easyocr
import numpy as np
from pyautogui import screenshot
from math import ceil
import keyboard
import json
import pypresence

rpc = True
DEBUG = True # Saves screenshots taken
counter = 0 # used with DEBUG
TargetKills: int

reader = easyocr.Reader(['en'])
import os; os.system("cls")
LastCriticalKills = 0

while True:
  try:
    with open("bo6 military tracker info.json", "r") as file:
      JsonInformation: dict = json.load(file)
    break
  except FileNotFoundError:
    if input("JSON file not found. Download? (y/n)").lower() == "y":
      import requests
      JsonInformation = requests.get(r"https://raw.githubusercontent.com/FlyingBacen/tiny-projects/main/bo6%20military%20tracker%20info.json").json()
      with open("bo6 military tracker info.json", "x") as file:
        json.dump(JsonInformation, file, indent = 2)
    else:
      input("This program requires a JSON file to function. Press enter to exit.")
      exit()

def SaveJsonInformation():
  global JsonInformation
  with open("bo6 military tracker info.json", "w") as file:
    json.dump(JsonInformation, file, indent = 2)

def changeTargets():
  global TargetKills, EnemiesPerRound, category, gun, SelectedCategory, SelectedGun, JsonInformation

  SaveJsonInformation()
  print("Weapon's Information saved to file.\n")

  Categories = list(JsonInformation["Weapons"].keys())
  for idx, category in enumerate(Categories):
    print(str(idx + 1) + ". " + category)
  SelectedCategory = Categories[int(input("Category: ")) - 1]

  Guns = list(JsonInformation["Weapons"][SelectedCategory].keys())
  for idx, gun in enumerate(Guns):
    TotalKills = JsonInformation["Weapons"][SelectedCategory][gun]
    print(str(idx + 1) + ". " + gun + ": " + (str(TotalKills) if TotalKills < 2000 else "Complete"))
  SelectedGun = Guns[int(input("Gun: ")) - 1]

  TargetKills = 2000 - JsonInformation["Weapons"][SelectedCategory][SelectedGun]

  EnemiesPerRound = int(input("Enemies per round: "))


def calculate() -> None:
  global TargetKills, EnemiesPerRound, LastCriticalKills, JsonInformation, SelectedCategory, SelectedGun, counter

  CriticalKillScreenshot = screenshot(region = (495, 625, 48, 23)) # Critical kills
  KillPercentScreenshot = screenshot(region = (669, 627, 47, 18)) # Kill percent
  print()

  try: 
    CriticalKills: str = reader.readtext(np.array(CriticalKillScreenshot))[0][1].replace("O", "0").replace(" ", "").replace("I", "1") # type: ignore
    CriticalKills: int = int(CriticalKills)
  except IndexError:
    try: #Try a tighter fit
      CriticalKillScreenshot_Small = screenshot(region = (495+15, 625, 34, 16))
      CriticalKills: str = reader.readtext(np.array(CriticalKillScreenshot_Small))[0][1].replace("O", "0").replace(" ", "").replace("I", "1") # type: ignore
      CriticalKills: int = int(CriticalKills)
    except IndexError:
      print("Error: OCR found no text for critical kills.")
      CriticalKillScreenshot_Small.save(f"./debug/debug_critical_kills-{counter}-no_text-small.png")
      counter += 1
      if DEBUG: CriticalKillScreenshot.save(f"./debug/debug_critical_kills-{counter}.png")
      return
  except ValueError:
    print("Error: OCR failed to read the critical kills.")
    print("Critical kills: " + str(CriticalKills))
    counter += 1
    if DEBUG: CriticalKillScreenshot.save(f"./debug/debug_critical_kills-{counter}.png")
    return
  
  try: 
    KillPercent: str = reader.readtext(np.array(KillPercentScreenshot))[0][1].replace(" ", "").replace("O", "0").replace("%", "").replace("I", "1").replace("\"", "") # type: ignore
    KillPercent: float = float(KillPercent) / 100
  except IndexError:
    print("Error: OCR found no text for kill percent.")
    counter += 1
    if DEBUG: KillPercentScreenshot.save(f"./debug/debug_kill_percent-{counter}.png")
    return
  except ValueError:
    print("Error: OCR failed to read the kill percent.")
    print("Kill percent: " + str(KillPercent))
    counter += 1
    if DEBUG: KillPercentScreenshot.save(f"./debug/debug_kill_percent-{counter}.png")
    return

  roundsLeft = ceil((int(TargetKills)-CriticalKills)*(1+abs(1-KillPercent))/int(EnemiesPerRound))
  if roundsLeft <= 10: print("remaining zombies: " + str(int(TargetKills)-CriticalKills))
  print("Estimated Rounds left: " + str(roundsLeft))

  if rpc:
    set_discord_rich_presence(1378753267105923123, f"{SelectedCategory} - {SelectedGun.capitalize()}", f"{roundsLeft} rounds left - {KillPercent}", "afterlife", "Made by <@717471432816459840>")
  difference = CriticalKills - LastCriticalKills
  JsonInformation["Weapons"][SelectedCategory][SelectedGun] += difference
  LastCriticalKills = CriticalKills

  # Use for debug
  # print(str(TargetKills) + " kills\n" + str(CriticalKills) + " critical kills\n" + str(KillPercent) + "% kill percent\n" + EnemiesPerRound + " enemies per round\n")

def set_discord_rich_presence(client_id, details, state, large_image=None, large_text=None):
  """
  Sets Discord Rich Presence using pypresence.

  Args:
    client_id (str): Your application's client ID.
    details (str): The first line of the presence.
    state (str): The second line of the presence.
    large_image (str, optional): Key of the large image asset.
    large_text (str, optional): Tooltip for the large image.
  """
  rpc = pypresence.Presence(client_id)
  rpc.connect()
  presence_data = {
    "details": details,
    "state": state,
  }
  if large_image:
    presence_data["large_image"] = large_image
  if large_text:
    presence_data["large_text"] = large_text
  rpc.update(**presence_data)

changeTargets()
keyboard.add_hotkey("+", calculate)
keyboard.add_hotkey("-", changeTargets)
try: keyboard.wait()
except KeyboardInterrupt: 
  with open("bo6 military tracker info.json", "w") as file:
    json.dump(JsonInformation, file, indent = 2)