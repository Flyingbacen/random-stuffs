import easyocr
import numpy as np
from pyautogui import screenshot
from math import ceil
import keyboard
import json

reader = easyocr.Reader(['en'])
print("\033[H\033[J")
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


def calculate():
  global TargetKills, EnemiesPerRound, LastCriticalKills, JsonInformation, SelectedCategory, SelectedGun

  CritKillScreenshot = screenshot(region = (495, 625, 543, 648)) # Critical kills
  KillPercentScreenshot = screenshot(region = (669, 627, 716, 645)) # Kill percent
  print()

  try: 
    CriticalKills = reader.readtext(np.array(CritKillScreenshot))[0][1].replace("O", "0").replace(" ", "").replace("I", "1") # type: ignore
    CriticalKills = int(CriticalKills)
  except IndexError: print("Error: OCR found no text for critical kills."); return
  except ValueError:
    print("Error: OCR failed to read the critical kills.")
    print("Critical kills: " + CriticalKills)
    return
  
  try: 
    KillPercent = reader.readtext(np.array(KillPercentScreenshot))[0][1].replace(" ", "").replace("O", "0").replace("%", "").replace("I", "1") # type: ignore
    KillPercent = float(KillPercent) / 100
  except IndexError: print("Error: OCR found no text for kill percent."); return
  except ValueError:
    print("Error: OCR failed to read the kill percent.")
    print("Kill percent: " + KillPercent)
    return

  roundsLeft = ceil((int(TargetKills)-CriticalKills)*(1+abs(1-KillPercent))/int(EnemiesPerRound))
  if roundsLeft < 10: print("remaining zombies: " + str(int(TargetKills)-CriticalKills))
  print("Estimated Rounds left: " + str(roundsLeft))

  difference = CriticalKills - LastCriticalKills
  JsonInformation["Weapons"][SelectedCategory][SelectedGun] += difference
  LastCriticalKills = CriticalKills

  # Use for debug
  # print(str(TargetKills) + " kills\n" + str(CriticalKills) + " critical kills\n" + str(KillPercent) + "% kill percent\n" + EnemiesPerRound + " enemies per round\n")


changeTargets()
keyboard.add_hotkey("+", calculate)
keyboard.add_hotkey("-", changeTargets)
try: keyboard.wait()
except KeyboardInterrupt: 
  with open("bo6 military tracker info.json", "w") as file:
    json.dump(JsonInformation, file, indent = 2)