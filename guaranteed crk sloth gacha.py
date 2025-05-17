import enum

Level = 1
PointsNeeded = 25000*min(max(Level, 1), 15) # keep between 1 and 15
# 100 points per pull, 250 pulls per level

class Points(enum.Enum):
    """referring to it as .points instead of .value to make it sound better :3"""
    @property
    def points(self):
        return self.value

# region tasks
class LightOfSlothTasks(Points):
    # PointsPerTask * AmountOfTasks + PointsOnFinishingGroup
    SugarSparklingWater=60*7+200
    MulledJuiceBaths=60*8+300
    LovelyToothling=60*10+300
    MarshmallowPavillion=70*11+400
    TheJewelryBox=70*12+400
    SugarBud=70*13+500
    TheBringersStatue=70*13+500
    TheHeart=80*15+700

# region other sources
class OtherSources(Points):
    FreeEternalPass=100+100+100+100+100+200 # Level: 1, 15, 25, 35, 40
    DailyGifts=100*12+200+300 # From new update, once per day for 14 days
    BossRush=300

# region paid sources
class PaidSources(Points):
    PaidEternalPass=1000+1000+1000+1000+2000 # Level: 1, 15, 25, 35, 40
    # all below: Amount * AmountOfTimesBought
    PaidSuperCrystalPackage=2200*5
    PaidGenerousShoppingBox=800*4
    PaidShop=800*9+1600*9+3600*9+6000*9+10800*9

# region dailies
class Dailies(Points):
    LightOfSlothDailyTask=40*4+70
    JuicyStaminaJellyChallenge=100
    FreeFromShop=40

# region non-dailies
def getNonDailiesDone(EternalPass: bool, whale: bool):

    totalPoints = sum([entry.points for entry in LightOfSlothTasks])
    totalPoints += sum([entry.points for entry in OtherSources])

    if EternalPass:
        totalPoints += PaidSources.PaidEternalPass.points
    if whale:
        totalPoints += sum([entry.points for entry in PaidSources]) - PaidSources.PaidEternalPass.points

    return totalPoints

# region do daily
def doDaily(CurrentPoints: int, CurrentDailies: int):

    CurrentPoints+=sum([entry.points for entry in Dailies])
    CurrentDailies+=1

    return CurrentPoints, CurrentDailies
    

PointsWithNoDailiesAndF2P = getNonDailiesDone(False, False)
PointsWithNoDailiesAndEternalPass = getNonDailiesDone(True, False)
PointsWithNoDailiesAndWhale = getNonDailiesDone(False, True)
PointsWithNoDailiesAndEternalPassAndShopWhale = getNonDailiesDone(True, True)

# region f2p
CurrentDailies = 0
while PointsWithNoDailiesAndF2P < PointsNeeded:
    PointsWithNoDailiesAndF2P, CurrentDailies = doDaily(PointsWithNoDailiesAndF2P, CurrentDailies) # This does cause the variable to have dailies, but shh
    # print(f"Current points: {PointsWithNoDailiesAndNotPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies and no Eternal Pass: {getNonDailiesDone(False, False)}")
print(f"Total dailies: {CurrentDailies}")

# region Eternal Pass
CurrentDailies = 0
while PointsWithNoDailiesAndEternalPass < PointsNeeded:
    PointsWithNoDailiesAndEternalPass, CurrentDailies = doDaily(PointsWithNoDailiesAndEternalPass, CurrentDailies)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies and Eternal Pass: {getNonDailiesDone(True, False)}")
print(f"Total dailies: {CurrentDailies}")

# region whale
CurrentDailies = 0
while PointsWithNoDailiesAndWhale < PointsNeeded:
    PointsWithNoDailiesAndWhale, CurrentDailies = doDaily(PointsWithNoDailiesAndWhale, CurrentDailies)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies, No Eternal Pass, and shop whale: {getNonDailiesDone(False, True)}")
print(f"Total dailies: {CurrentDailies}")

# region Eternal Pass and shop whale
CurrentDailies = 0
while PointsWithNoDailiesAndEternalPassAndShopWhale < PointsNeeded:
    PointsWithNoDailiesAndEternalPassAndShopWhale, CurrentDailies = doDaily(PointsWithNoDailiesAndEternalPassAndShopWhale, CurrentDailies)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies, Eternal Pass, and shop whale: {getNonDailiesDone(True, True)}")
print(f"Total dailies: {CurrentDailies}")