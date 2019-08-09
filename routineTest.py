import time
import json
from CustomRobot import CustomRobot
from onrobot_rg2_gripper import OnRobotGripperRG2
import collisions
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import sys
from robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
from routines import *
import atexit
import routines

tcps = {
    "hand": (0, 0, 0.1595, 0, 0,  0),
    "spatula": (-0.00787, -0.2537, 0.160, 0, 0, 0),
    "oil": (0, 0, 0, 0, 0, 0),
    "ladle": (-0.042164, -0.073406, 0.346456, 0, 0, 0),
    "toppings": (.02794, 0, 0.12192, 0, 0, 0)
}

robot = CustomRobot.connect(json.load(open('config.json'))["ip"])
robot.hand = Robotiq_Two_Finger_Gripper(robot)
robot.set_tcp(tcps["hand"])
time.sleep(1)
robot.hand.activate_gripper()

def exit_handler():
    print('program exiting')
    robot.close()

atexit.register(exit_handler)

routines.setRobot(robot)
robot.set_tcp(tcps["hand"])

goHome()
hopen()
getDrySpatula()
robot.set_tcp(tcps["spatula"])
pickUpEgg()
plateEgg()
putAwayDrySpatula()
