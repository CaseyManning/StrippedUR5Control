# import urx
import time
import json
from CustomRobot import CustomRobot
import routines
import os
import sys
from robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper
from routines import tcps
import atexit
from routines import *
import routines

tcps = {
    "hand": (0, 0, 0.1595, 0, 0,  0)
}

robot = CustomRobot.connect(json.load(open('config.json'))["ip"])
robot.hand = Robotiq_Two_Finger_Gripper(robot)
robot.set_tcp(tcps["hand"])
time.sleep(1)

def exit_handler():
    robot.close()

atexit.register(exit_handler)

routines.setRobot(robot)

robot.hand.activate_gripper()
exampleWaypoint()