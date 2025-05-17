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

    return totalPoints

# region do daily
def doDaily(CurrentPoints: int, CurrentDailies: int, EternalPass: bool):

    CurrentPoints+=sum([entry.points for entry in Dailies.Standard])
    if EternalPass:
        CurrentPoints+=Dailies.PaidEternalPassRewardLandmark.points
    CurrentDailies+=1

    return CurrentPoints, CurrentDailies
            

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
EternalPassMaster = getNonDailiesDone(
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
while F2P < PointsNeeded:
    F2P, CurrentDailies = doDaily(F2P, CurrentDailies, False)
    # print(f"Current points: {PointsWithNoDailiesAndNotPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies and no Eternal Pass: {getNonDailiesDone(EternalPass=False, EternalPassMaster=False, Whale=False )}")
print(f"Total dailies: {CurrentDailies}")

# region Eternal Pass
CurrentDailies = 0
while EternalPass < PointsNeeded:
    EternalPass, CurrentDailies = doDaily(EternalPass, CurrentDailies, True)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies and Eternal Pass: {getNonDailiesDone(EternalPass=True, EternalPassMaster=False, Whale=False)}")
print(f"Total dailies: {CurrentDailies}")

# region Eternal Pass and Master Hot Deal Package
CurrentDailies = 0
while EternalPassMaster < PointsNeeded:
    EternalPassMaster, CurrentDailies = doDaily(EternalPassMaster, CurrentDailies, True)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies and Eternal Pass Master: {getNonDailiesDone(EternalPass=True, EternalPassMaster=True, Whale=False)}")
print(f"Total dailies: {CurrentDailies}")

# region whale
CurrentDailies = 0
while Whale < PointsNeeded:
    Whale, CurrentDailies = doDaily(Whale, CurrentDailies, False)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies, No Eternal Pass, and shop whale: {getNonDailiesDone(EternalPass=False, EternalPassMaster=False, Whale=True)}")
print(f"Total dailies: {CurrentDailies}")

# region Eternal Pass and shop whale
CurrentDailies = 0
while EternalPassAndWhale < PointsNeeded:
    EternalPassAndWhale, CurrentDailies = doDaily(EternalPassAndWhale, CurrentDailies, True)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies, Eternal Pass, and shop whale: {getNonDailiesDone(EternalPass=True, EternalPassMaster=False, Whale=True,) }")
print(f"Total dailies: {CurrentDailies}")

# region Eternal Pass Master and shop whale
CurrentDailies = 0
while EternalPassMasterAndWhale < PointsNeeded:
    EternalPassMasterAndWhale, CurrentDailies = doDaily(EternalPassMasterAndWhale, CurrentDailies, True)
    # print(f"Current points: {PointsWithNoDailiesAndPaid}, Current dailies: {CurrentDailies}")
print(f"Total points with no dailies, Eternal Pass Master, and shop whale: {getNonDailiesDone(EternalPass=True, EternalPassMaster=True, Whale=True)}")
print(f"Total dailies: {CurrentDailies}")