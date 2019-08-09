# import urx
import time
import json
from CustomRobot import CustomRobot
from onrobot_rg2_gripper import OnRobotGripperRG2
import routines
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import sys
from robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
from routines import tcps
import atexit
import maker
import logger
from maker import makeOmelette
import traceback

robot = CustomRobot.connect(json.load(open('config.json'))["ip"])
robot.hand = Robotiq_Two_Finger_Gripper(robot)
robot.set_tcp(tcps["hand"])
time.sleep(1)

beCareful = True

logger.startFileLogging()

TEST_MODE = True
useVision = False
rerun = False

def exit_handler():
    robot.close()

atexit.register(exit_handler)

routines.setRobot(robot)
maker.setRobot(robot)

toppings = True
cheese = True
assert beCareful == True, "Don't Spill the Egg!"

if TEST_MODE:
    f = open("saveState.txt", "r")
    text = f.read()
    try:
        if text == '' or not rerun:
            logger.log('Starting new Omelette')
            robot.hand.activate_gripper()
            makeOmelette(robot, toppings=toppings, cheese=cheese, useVision=useVision)
        else:
            logger.log('Restarting from where we left off at routine ' + text[:text.index('\n')] + ', waypoint ' + text[text.index('\n') + 1:])
            makeOmelette(robot, toppings=toppings, cheese=cheese, saveState=text, useVision=useVision)
    except Exception as e:
        ex_type, ex, tb = sys.exc_info()
        foo = traceback.extract_tb(tb).format()
        for item in foo:
            logger.log(item.replace("\n", " "))
        logger.log(str(e))
    logger.log("test done")

    f = open("saveState.txt", "w")
    f.write('')
    f.close()

    robot.close()
    sys.exit(0)

# Firebase stuff below

def setStatus(db, id, status):
    order = db.collection(u'orders').document(id)

    order.set({
        u'Status': status
    }, merge=True)

project_id = 'scrambldapp'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="scrambldapp-2f037a06600b.json"
orders = []
ids = []

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
'projectId': project_id,
})

db = firestore.client()

while True:
    time.sleep(3)
    users_ref = db.collection(u'orders')
    docs = users_ref.get()
    orders = []
    ids = []
    print('Getting orders from Firebase')

    for doc in docs:
        if doc.to_dict()["Status"] == "Queued":
            orders.append(doc.to_dict())
            ids.append(doc.id)
        try:
            cheese = doc.to_dict()["Cheese"]
            toppings = doc.to_dict()["Toppings"]
        except:
            pass

    if len(orders) > 0:
        print('Making Omelette ' + str(orders[0]['id']))
        setStatus(db, ids[0], "Cooking")
        while True:
            try:
                f = open("saveState.txt", "r")
                text = f.read()
                if text == '' or not rerun:
                    logger.log('Starting new Omelette')
                    robot.hand.activate_gripper()
                    makeOmelette(robot, toppings=toppings, cheese=cheese, useVision=useVision)
                else:
                    logger.log('Restarting from where we left off at routine ' + text[:text.index('\n')] + ', waypoint ' + text[text.index('\n') + 1:])
                    makeOmelette(robot, toppings=toppings, cheese=cheese, saveState=text, useVision=useVision)
            except KeyboardInterrupt:
                sys.exit(0)
                break
            except Exception as e:
                logger.log(str(e))
        setStatus(db, ids[0], "Done")
