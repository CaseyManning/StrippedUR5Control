import json
from CustomRobot import CustomRobot
import pygame
import time
import numpy as np
import math
from robotiq_two_finger_gripper import Robotiq_Two_Finger_Gripper

pygame.init()

config = json.load(open('config.json'))
robot = CustomRobot.connect(config["ip"])
hand = Robotiq_Two_Finger_Gripper(robot)
robot.hand = hand
handTCP = (0, 0, 0.211, 0, 0, 0)
# robot.set_tcp(handTCP)

relativeMovement = [0, 0, 0, 0, 0, 0]

screen = pygame.display.set_mode([255, 255])
pygame.display.set_caption("Robot Controller")
done = False

close = False
cooldown = .2
incPress = time.time()

increment = 0.001 
acc=linAcc = 0.1

def printIncrement():
    print("new increment: "+ str(increment * 1000) + " mm")

printIncrement()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        print('+ X | left')
        robot.move_relative(increment, 0, 0, acc=linAcc)
        relativeMovement[0] += increment
    if keys[pygame.K_RIGHT]:
        print('- X | right')
        relativeMovement[0] -= increment
        robot.move_relative(-increment, 0, 0, acc=linAcc)
    if keys[pygame.K_UP]:
        print('+ Y | up')
        relativeMovement[1] += increment
        robot.move_relative(0, increment, 0, acc=linAcc)
    if keys[pygame.K_DOWN]:
        print('- Y | down')
        relativeMovement[1] -= increment
        robot.move_relative(0, -increment, 0, acc=linAcc)
    if keys[pygame.K_SLASH]:
        print('+ Z | slash')
        relativeMovement[2] += increment
        robot.move_relative(0, 0, increment, acc=linAcc)
    if keys[pygame.K_RSHIFT]:
        print('- Z | shift')
        relativeMovement[2] -= increment
        robot.move_relative(0, 0, -increment, acc=linAcc)


    if keys[pygame.K_w]:
        print('+ RX | w')
        relativeMovement[3] += increment
        robot.move_relativeb(0, 0, 0, increment, 0, 0)
    if keys[pygame.K_s]:
        print('- RX | s')
        relativeMovement[3] -= increment
        robot.move_relativeb(0, 0, 0, -increment, 0, 0)
    if keys[pygame.K_a]:
        print('+ RY | a')
        relativeMovement[4] += increment
        robot.move_relativeb(0, 0, 0, 0, increment, 0)
    if keys[pygame.K_d]:
        print('- RY | d')
        relativeMovement[4] -= increment
        robot.move_relativeb(0, 0, 0, 0, -increment, 0)
    if keys[pygame.K_q]:
        print('+ RZ | q')
        relativeMovement[5] += increment
        robot.move_relativeb(0, 0, 0, 0, 0, increment)
    if keys[pygame.K_e]:
        print('- RZ | e')
        relativeMovement[5] -= increment
        robot.move_relativeb(0, 0, 0, 0, 0, -increment)

    if keys[pygame.K_SPACE]:
        print('hand | space')
        if close:
            robot.hand.open_gripper(128)
            close = False
        else:
            robot.hand.close_gripper()
            close = True

    if keys[pygame.K_j] and time.time() > (incPress + cooldown):
        incPress = time.time()
        degs = []
        for value in robot.getj():
            degs.append(round(math.degrees(value), 2))
        print('joints (deg) | j')
        print(degs)

    if keys[pygame.K_p] and time.time() > (incPress + cooldown): # broken
        incPress = time.time()
        print('TCP\'s Pose THIS IS CURRENTLY BROKEN FIX IT IDK WHY IT WONT WORK T_T | p')
        print(str(robot.get_pose()))

    if keys[pygame.K_r] and time.time() > (incPress + cooldown):
        incPress = time.time()
        print(relativeMovement)

    if keys[pygame.K_PERIOD] and time.time() > (incPress + cooldown):
        incPress = time.time()
        increment += 0.001
        printIncrement()
    if keys[pygame.K_COMMA] and time.time() > (incPress + cooldown):
        incPress = time.time()
        increment -= 0.001
        printIncrement()
    if keys[pygame.K_RETURN] and time.time() > (incPress + cooldown):
        incPress = time.time()
        increment = float(input("Enter the desired increment in mm: ")) / 1000
        printIncrement()
    if keys[pygame.K_BACKQUOTE] and time.time() > (incPress + cooldown):
        incPress = time.time()
        position = eval(input("Enter the joint position: "))
        robot.move_absolute_j(*position, 3, 3, degrees=True)

    pygame.display.flip()
