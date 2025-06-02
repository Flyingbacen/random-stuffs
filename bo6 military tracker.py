import easyocr
import numpy as np
from pyautogui import screenshot
from math import ceil
import keyboard
import json
import pypresence
import time

Usewzhub = True
if Usewzhub:
  import requests
  try:
    with open("bo6config.json", "r") as file:
      bo6config = json.load(file)
  except FileNotFoundError:
    Usewzhub = False


rpc = False
starttime = time.time() 
DEBUG = True # Saves screenshots taken
counter = 0 # used with DEBUG
TargetKills: int
milestones = [100, 200, 300, 400, 600, 800, 1000, 1500, 2000]

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

      with open("bo6 military tracker info.json", "r") as file: # Set all weapons to 0
        data = json.load(file)

      for category in data["Weapons"]:
        for weapon in data["Weapons"][category]:
          data["Weapons"][category][weapon] = 0

      with open("bo6 military tracker info upload.json", "w") as file:
        json.dump(data, file, indent=2)
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
    set_discord_rich_presence(1378753267105923123, f"{SelectedCategory} - {SelectedGun.capitalize()}", f"{str(roundsLeft)} rounds left - {str(KillPercent*100)}% Critical Kill accuracy", "gold", "Made by @Flyingbacen on Github")
  
  difference = CriticalKills - LastCriticalKills
  JsonInformation["Weapons"][SelectedCategory][SelectedGun] += difference
  LastCriticalKills = CriticalKills

  if Usewzhub:
    # Check if a milestone was passed
    previous_kills = JsonInformation["Weapons"][SelectedCategory][SelectedGun] - difference
    current_kills = JsonInformation["Weapons"][SelectedCategory][SelectedGun]
    for idx, milestone in enumerate(milestones):
      if previous_kills < milestone <= current_kills:
        updateWZHub(SelectedGun, idx)

  # Use for debug
  # print(str(TargetKills) + " kills\n" + str(CriticalKills) + " critical kills\n" + str(KillPercent) + "% kill percent\n" + EnemiesPerRound + " enemies per round\n")

def set_discord_rich_presence(client_id, details, state, large_image=None, large_text=None):
  """
  Sets Discord Rich Presence using pypresence.<br>
  *WIP, doesn't work properly*

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
    "start": int(starttime)
  }
  if large_image:
    presence_data["large_image"] = large_image
  if large_text:
    presence_data["large_text"] = large_text
  rpc.update(**presence_data)

def updateWZHub(weapon: str, milestone: int) -> None:
  try:
    with open("bo6 military wzhub id's.json", "r") as File:
      WZHubWeaponInfo = json.load(File)
  except FileNotFoundError:
    print("WZHub weapon info file not found.")
    return
  items = WZHubWeaponInfo["data"][0]["items"]
  combined = {}

  # Combine favorited and unfavorited objects
  for key in set(items["unselected"].keys()).union(items["selected"].keys()):
    combined[key] = (items["unselected"].get(key, []) + items["selected"].get(key, []))
  Weapons = combined["orion"]

  # Find the id
  for weapon_info in Weapons:
    if weapon_info["info"]["name"] == weapon:
      weapon_id = weapon_info["camouflages"][milestone]["id"]
      if milestone >= 8:
        print("Unique challenges:")
        print(weapon_info["camouflages"][9]["unlock"]["action"])
        print(weapon_info["camouflages"][10]["unlock"]["action"])
      break
    
  if not weapon_id:
    print("Could not find id")
  
  url = bo6config["url"]
  headers = {
    "authorization": bo6config["authorization"],
    "x-xsrf-token": bo6config["x-xsrf-token"],
    "Cookie": f"XSRF-TOKEN={bo6config["x-xsrf-token"]}; wzhub_session={bo6config["wzhub_session"]}",
    "content-type": "application/json",
    "origin": "https://wzhub.gg",
    "priority": "u=1, i",
    "referer": "https://wzhub.gg/",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 OPR/118.0.0.0"
  }
  body = [
    {
      "id": weapon_id,
      "state": True
    }
  ]

  response = requests.post(url=url, json=body, headers=headers)
  try:
    if response.json()["success"] and response.status_code == 200:
      print("\nSuccessfully updated WZhub")
    else:
      print(response)
  except json.JSONDecodeError:
    source = response.text
    if "\"/login\" method=\"post\"" in source:
      print("Authorization likely expired. Re-set authorization Bearer")


changeTargets()
keyboard.add_hotkey("+", calculate)
keyboard.add_hotkey("-", changeTargets)
try: keyboard.wait()
except KeyboardInterrupt: 
  with open("bo6 military tracker info.json", "w") as file:
    json.dump(JsonInformation, file, indent = 2)