from routines import *
import routines
import time
import eggClassifier

tcps = {
    "hand": (0, 0, 0.1595, 0, 0,  0),
    "oil": (0, 0, 0, 0, 0, 0),
    "toppings": (.02794, 0, 0.12192, 0, 0, 0),
    "spatula": (-0.00787, -0.2537, 0.160, 0, 0, 0),
    "ladle": (-0.042164, -0.073406, 0.346456, 0, 0, 0)
}

def makeOmelette(robot, toppings=True, cheese=True, saveState=None, useVision=False):
    print('we making the omelette')
    if not saveState == None:
        routines.reachedSaveRoutine = False
        routines.reachedSaveWaypoint = False
        routines.saveRoutine = saveState[:saveState.index('\n')]
        routines.saveWaypoint = saveState[saveState.index('\n') + 1:]

    if useVision:
        eggClassifier.startClassificationThread()

    goHome()
    turnOnPanToppings()
    goHome()
    heatUpPan()
    goHome()

    hopen()
    getOil()
    robot.set_tcp(tcps["oil"])
    pourOil()
    putAwayOil()
    robot.set_tcp(tcps["hand"])

    if toppings:
        goHome()
        getToppings()
        robot.set_tcp(tcps["toppings"])
        pourToppings()
        putAwayToppings()
        robot.set_tcp(tcps["hand"])

        goHome()
        getWetSpatula()
        robot.set_tcp(tcps["spatula"])
        stir()
        putAwayWetSpatula()
        robot.set_tcp(tcps["hand"])
    
    decreaseTemperature()
    goHome()
    hopen()
    getLadle()
    robot.set_tcp(tcps["ladle"])
    wipeLadle()
    pourEgg()
    putAwayLadle()
    robot.set_tcp(tcps["hand"])

    goHome()
    getWetSpatula()
    robot.set_tcp(tcps["spatula"])

    if useVision:
        keepStirring = True
        maxStirCount = 6
        numStirs = 0

        while keepStirring and numStirs < maxStirCount:
            stir()
            numStirs += 1
            time.sleep(3.5)
            print("Overall prediction: " + str(eggClassifier.getPrediction()))
            keepStirring = (eggClassifier.getPrediction() == "stir") or numStirs < 3

    else:
        for i in range(6):
            stir()


    if cheese:
        putAwayWetSpatula()
        robot.set_tcp(tcps["hand"])
        getCheese()
        pourCheese()
        putAwayCheese()
        getWetSpatula()
        robot.set_tcp(tcps["spatula"])
    else:
        cheeseSleep()

    pickUpEgg()
    flipEgg()
    putAwayWetSpatula()
    robot.set_tcp(tcps["hand"])

    flipSleep()

    getDrySpatula()
    robot.set_tcp(tcps["spatula"])
    pickUpEgg()
    plateEgg()
    robot.set_tcp(tcps["hand"])
    putAwayDrySpatula()

    goHome()
    turnOffPan()
    goHome()