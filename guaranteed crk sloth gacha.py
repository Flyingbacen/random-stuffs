import enum

Level = 1
PointsNeeded = 25000*min(max(Level, 1), 15) # keep between 1 and 15
# 100 points per pull, 250 pulls per level

class Points(enum.Enum):
    """referring to it as .points instead of .value to make it sound better :3"""
    @property
    def points(self):
        return self.value

class OneTimeSources(Points):
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
        BossRush=100+200+700 # Stage: 3, 7, 25
        MonsterMenace=1000 # Level 8
    
    class PathOfSlothTasks(Points):
        # Assuming that you will do these missions once you obtain her
        LVL1=200*4
        
        # counting the 2* mission from LVL 1 since that will most likely only be done after the rest are complete
        LVL2=2000+400*4

        # Same as above for 4*
        LVL3=4000+600*5

    # region paid sources
    class PaidSources(Points):
        class EternalPass(Points):
            PaidEternalPass=1000+1000+1000+1000+2000 # Level: 1, 15, 25, 35, 40}
            PaidEternalPassMasterHotDealPackage=1000 # Oppurtunity to buy after completing the pass
            
        class Whale(Points):
            # Amount * AmountOfTimesBought
            PaidSuperCrystalPackage=2200*5
            PaidGenerousShoppingBox=800*4
            PaidShop=800*9+1600*9+3600*9+6000*9+10800*9

        EternalSugarCookieFirstGreetings=1000 
        # Almost certainly you will get some after promoting to 1* too, but I'm too lazy to research that
        # Only got that info cause I got her :3

# region dailies
class Dailies(Points):
    class Standard(Points):
        LightOfSlothDailyTask=40*4+70
        JuicyStaminaJellyChallenge=100
        FreeFromShop=40

    PaidEternalPassRewardLandmark=100 # Sleepy Pavlova Hanging Garden

# region non-dailies
def getNonDailiesDone(EternalPass: bool, EternalPassMaster: bool, Whale: bool):

    totalPoints = sum([entry.points for entry in OneTimeSources.LightOfSlothTasks])
    totalPoints += sum([entry.points for entry in OneTimeSources.OtherSources])

    if EternalPass:
        totalPoints += OneTimeSources.PaidSources.EternalPass.PaidEternalPass.points
        if EternalPassMaster:
            totalPoints += OneTimeSources.PaidSources.EternalPass.PaidEternalPassMasterHotDealPackage.points
    if Whale:
        totalPoints += sum([entry.points for entry in OneTimeSources.PaidSources.Whale])
        totalPoints += OneTimeSources.PaidSources.EternalSugarCookieFirstGreetings.points

    return totalPoints

# region do daily
def doDaily(CurrentPoints: int, CurrentDailies: int, EternalPass: bool, LVL1: bool = False, LVL2: bool = False, LVL3: bool = False):

    CurrentPoints+=sum([entry.points for entry in Dailies.Standard])
    if EternalPass:
        CurrentPoints+=Dailies.PaidEternalPassRewardLandmark.points
    CurrentDailies+=1

    if CurrentPoints >= 25000 and not LVL1:
        CurrentPoints += OneTimeSources.PathOfSlothTasks.LVL1.points
        LVL1 = True
    if CurrentPoints >= 75000 and not LVL2:
        CurrentPoints += OneTimeSources.PathOfSlothTasks.LVL2.points
        LVL2 = True
    if CurrentPoints >= 125000 and not LVL3:
        CurrentPoints += OneTimeSources.PathOfSlothTasks.LVL3.points
        LVL3 = True

    return CurrentPoints, CurrentDailies, LVL1, LVL2, LVL3
            

F2P = getNonDailiesDone(
    EternalPass=False,
    EternalPassMaster=False,
    Whale=False
)
EternalPass = getNonDailiesDone(
    EternalPass=True,
    EternalPassMaster=False,
    Whale=False
)
EternalPassMaster = getNonDailiesDone( # Assuming that you will only buy this if you buy the pass
    EternalPass=True,
    EternalPassMaster=True,
    Whale=False
)
Whale = getNonDailiesDone(
    EternalPass=False,
    EternalPassMaster=False,
    Whale=True
)
EternalPassAndWhale = getNonDailiesDone(
    EternalPass=True,
    EternalPassMaster=False,
    Whale=True
)
EternalPassMasterAndWhale = getNonDailiesDone(
    EternalPass=True,
    EternalPassMaster=True,
    Whale=True
)

# region f2p
CurrentDailies = 0
LVL1, LVL2, LVL3 = False, False, False
while F2P < PointsNeeded:
    F2P, CurrentDailies, LVL1, LVL2, LVL3 = doDaily(F2P, CurrentDailies, False, LVL1, LVL2, LVL3)
    # print(f"Current points: {PointsWithNoDailiesAndNotPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies and no Eternal Pass: {getNonDailiesDone(EternalPass=False, EternalPassMaster=False, Whale=False )}")
print(f"Total dailies: {CurrentDailies}")

# region Eternal Pass
CurrentDailies = 0
LVL1, LVL2, LVL3 = False, False, False
while EternalPass < PointsNeeded:
    EternalPass, CurrentDailies, LVL1, LVL2, LVL3 = doDaily(EternalPass, CurrentDailies, True, LVL1, LVL2, LVL3)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies and Eternal Pass: {getNonDailiesDone(EternalPass=True, EternalPassMaster=False, Whale=False)}")
print(f"Total dailies: {CurrentDailies}")

# region Eternal Pass and Master Hot Deal Package
CurrentDailies = 0
LVL1, LVL2, LVL3 = False, False, False
while EternalPassMaster < PointsNeeded:
    EternalPassMaster, CurrentDailies, LVL1, LVL2, LVL3 = doDaily(EternalPassMaster, CurrentDailies, True, LVL1, LVL2, LVL3)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies and Eternal Pass Master: {getNonDailiesDone(EternalPass=True, EternalPassMaster=True, Whale=False)}")
print(f"Total dailies: {CurrentDailies}")

# region whale
CurrentDailies = 0
LVL1, LVL2, LVL3 = False, False, False
while Whale < PointsNeeded:
    Whale, CurrentDailies, LVL1, LVL2, LVL3 = doDaily(Whale, CurrentDailies, False, LVL1, LVL2, LVL3)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies, No Eternal Pass, and shop whale: {getNonDailiesDone(EternalPass=False, EternalPassMaster=False, Whale=True)}")
print(f"Total dailies: {CurrentDailies}")

# region Eternal Pass and shop whale
CurrentDailies = 0
LVL1, LVL2, LVL3 = False, False, False
while EternalPassAndWhale < PointsNeeded:
    EternalPassAndWhale, CurrentDailies, LVL1, LVL2, LVL3 = doDaily(EternalPassAndWhale, CurrentDailies, True, LVL1, LVL2, LVL3)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies, Eternal Pass, and shop whale: {getNonDailiesDone(EternalPass=True, EternalPassMaster=False, Whale=True,) }")
print(f"Total dailies: {CurrentDailies}")

# region Eternal Pass Master and shop whale
CurrentDailies = 0
LVL1, LVL2, LVL3 = False, False, False
while EternalPassMasterAndWhale < PointsNeeded:
    EternalPassMasterAndWhale, CurrentDailies, LVL1, LVL2, LVL3 = doDaily(EternalPassMasterAndWhale, CurrentDailies, True, LVL1, LVL2, LVL3)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies, Eternal Pass Master, and shop whale: {getNonDailiesDone(EternalPass=True, EternalPassMaster=True, Whale=True)}")
print(f"Total dailies: {CurrentDailies}")