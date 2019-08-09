import json
import time
import logger

routines = {}
config = json.load(open('config.json'))
routinePoints = json.load(open('routinePoints.json'))


tcps = {
    "hand": (0, 0, 0.1595, 0, 0,  0),
    "spatula": (-0.00787, -0.2537, 0.160, 0, 0, 0),
    "oil": (0, 0, 0, 0, 0, 0),
    "ladle": (-0.042164, -0.073406, 0.346456, 0, 0, 0),
    "toppings": (.02794, 0, 0.12192, 0, 0, 0)
}

robot = None
reachedSaveRoutine = True
reachedSaveWaypoint = True
saveRoutine = None
saveWaypoint = None
clock = time.time()

num = 0

def setRobot(r):
    global robot
    robot = r


class Routine():
    num = 0
    def __init__(self, name):
        self.moves = []
        self.moveNames = []
        self.moveTypes = []
        self.name = name

    def addMove(self, move, typ, name):
        self.moves.append(move)
        self.moveTypes.append(typ)
        self.moveNames.append(name)

    def __call__(self):
        global num
        global robot
        global reachedSaveRoutine
        global reachedSaveWaypoint
        global saveRoutine
        global saveWaypoint
        logger.log(str(Routine.num) + ' | ' + self.name)
        if saveRoutine != None and Routine.num == int(saveRoutine):
            reachedSaveRoutine = True
        if not reachedSaveRoutine:
            reachedSaveWaypoint = False
            [robot.set_tcp(tcps[self.moves[x]]) for x in [index for index, value in enumerate(self.moveTypes) if value == 'tcp']]

            logger.log('skpping already completed routine ' + str(time.time() - clock))
            Routine.num += 1
            return
        for i in range(len(self.moves)):
            # print(self.moves[i])
            logger.log(self.moveNames[i])
            if reachedSaveWaypoint or self.moveTypes[i] == 'tcp':
                f = open("saveState.txt", "w")
                f.write(str(Routine.num) + '\n')
                f.write(self.moveNames[i])
                f.close()
                if self.moveTypes[i] == 'l':
                    robot.move_absolute(*tuple(self.moves[i]))
                elif self.moveTypes[i] == 'j':
                    robot.move_absolute_j(*tuple(self.moves[i]), degrees=True)
                elif self.moveTypes[i] == 'r':
                    robot.move_relativeb(*tuple(self.moves[i]))
                elif self.moveTypes[i] == 'gripper':
                    if self.moves[i] == 'close':
                        logger.log('closing gripper')
                        robot.hand.close_gripper()
                    else:
                        logger.log('opening gripper')
                        robot.hand.open_gripper(128)
                elif self.moveTypes[i] == 'tcp':
                    robot.set_tcp(tcps[self.moves[i]])
                    logger.log("set tcp " + self.moves[i])
                    robot.move_absolute_j(*robot.getj(), wait=False)
                elif self.moveTypes[i] == 'wait':
                    logger.log('sleeping for ' + str(self.moves[i]) + ' seconds.')
                    time.sleep(self.moves[i])
                else:
                    logger.log('ERROR: Unknown command type ' + self.moveTypes[i])
            if self.moveNames[i] == saveWaypoint:
                logger.log('We have reached the starting waypoint')
                logger.log("time taken: " + str(time.time() - clock))
                reachedSaveWaypoint = True
        Routine.num += 1

for foo, routine in routinePoints.items():
    rt = Routine(foo)
    for name, action in routine.items():
        if type(action) is list:
            if max(action) > 10:
                rt.addMove(action, 'j', name)
            else:
                rt.addMove(action, 'r', name)
        elif type(action) is int or type(action) is float:
            rt.addMove(action, 'wait', name)
        elif "rp" in name:
            if max(routinePoints[action][name[3:]]) > 10:
                rt.addMove(routinePoints[action][name[3:]], 'j', name)
            else:
                rt.addMove(routinePoints[action][name[3:]], 'r', name)
        else:
            rt.addMove(action, name, name)

    routines[foo] = rt

for name, routine in routines.items():
    globals()[name] = routine