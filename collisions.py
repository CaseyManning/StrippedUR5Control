import numpy as np
import math
import kinematics
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
mat=np.matrix
import time
# import ikfastpy
# Initialize kinematics for UR5 robot arm
armWidths = [.058, .058, .058, .048, .0375, .0375, .0375]
SMALL_NUM = 10**-8
TOLERANCE = 0.01   # tolerance for safe movement between arms in meters
global collisions
collisions = []

'''
Returns true if a collision is detected
'''
def collision(robot):
    collisions.clear()
    jps = robot.getj()

    angles = mat([[jps[0]], [jps[1]], [jps[2]], [jps[3]], [jps[4]], [jps[5]]])
    jointPositions = kinematics.HTrans(angles, [0])

    for i in range(len(jointPositions)-1):
        for j in range(len(jointPositions)-1):
            if abs(i - j) > 1:
                if distanceBetweenLines(np.array(jointPositions[i]), np.array(jointPositions[i+1]), np.array(jointPositions[j]), np.array(jointPositions[j+1])) < (armWidths[i] + armWidths[j] + TOLERANCE):
                    print("Collides between link " + str(i) + " and link " + str(j))
                    print(distanceBetweenLines(np.array(jointPositions[i]), np.array(jointPositions[i+1]), np.array(jointPositions[j]), np.array(jointPositions[j+1])))
                    print(armWidths[i] + armWidths[j] + TOLERANCE)
                    collisions.append(i)
                    collisions.append(j)
                    return True
    return False


def distanceBetweenLines(a1, a2, b1, b2):
    u = a2 - a1
    v = b2 - b1
    w = a1 - b1
    a = np.dot(u, u)
    b = np.dot(u, v)
    c = np.dot(v, v)
    d = np.dot(u, w)
    e = np.dot(v, w)
    D = a*c - b*b
    sc = D
    sN = D
    sD = D
    tc = D
    tN = D
    tD = D

    # compute the line parameters of the two closest points
    if D < SMALL_NUM:   # the lines are almost parallel
        sN = 0.0        # force using point a1 on segment a
        sD = 1.0        # to prevent possible division by 0.0 later
        tN = e
        tD = c
    else:               # get the closest points on the infinite lines
        sN = b*e - c*d
        tN = a*e - b*d
        if sN < 0.0:    # sc < 0 => the s = 0 edge is visible
            sN = 0.0
            tN = e
            tD = c
        elif sN > sD:   # sc > 1 => the s = 1 edge is visible
            sN = sD
            tN = e + b
            tD = c

    if tN < 0.0:  # tc < 0 => the t = 0 edge is visible
        tN = 0.0
        # recompute sc for this edge
        if -d < 0.0:
            sN = 0.0
        elif -d > a:
            sN = sD
        else:
            sN = -d
            sD = a
    elif tN > tD:  # tc > 1 => the t = 1 edge is visible
        tN = tD
        subbd = -d + b
        # recompute sc for this edge
        if subbd < 0.0:
            sN = 0
        elif subbd > a:
            sN = sD
        else:
            sN = subbd
            sD = a

    # finally do the division to get sc and tc
    if math.fabs(sN) < SMALL_NUM:
        sc = 0.0
    else:
        sc = sN / sD

    if math.fabs(tN) < SMALL_NUM:
        tc = 0.0
    else:
        tc = tN / tD

    # get the difference of the closest points
    dP = w + sc*u - tc*v  # = a(sc) - b(tc)

    return np.sqrt(np.dot(dP, dP))  # returns the length of the vector


def collisionCheck(robot):
    while True:
        if collision(robot):
            print("Collision!")
            print(np.rad2deg(robot.getj()))
            print("(degrees)")
            robot.uhoh = True
            time.sleep(1)
            # displayJoints(robot)
        # else:
        #     print("False")
    return True


def displayJoints(robot):
    jps = robot.getj()

    angles = mat([[jps[0]], [jps[1]], [jps[2]], [jps[3]], [jps[4]], [jps[5]]])
    jointPositions = kinematics.HTrans(angles, [0])
    # pyplot.ion()
    fig = pyplot.figure()
    ax = Axes3D(fig)
    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([0,1])

    print(jointPositions)

    ax.plot([0,jointPositions[0][0]], [0,jointPositions[0][1]],zs=[0,jointPositions[0][2]], color="blue")
    for i in range(len(jointPositions)-1):
        if i in collisions:
            ax.plot([jointPositions[i][0],jointPositions[i+1][0]], [jointPositions[i][1],jointPositions[i+1][1]],zs=[jointPositions[i][2],jointPositions[i+1][2]], color="red")
        else:
            ax.plot([jointPositions[i][0],jointPositions[i+1][0]], [jointPositions[i][1],jointPositions[i+1][1]],zs=[jointPositions[i][2],jointPositions[i+1][2]], color="blue")

    ax.scatter([jointPositions[0][0], jointPositions[1][0], jointPositions[2][0], jointPositions[3][0], jointPositions[4][0], jointPositions[5][0]],
        [jointPositions[0][1], jointPositions[1][1], jointPositions[2][1], jointPositions[3][1], jointPositions[4][1], jointPositions[5][1]],
        [jointPositions[0][2], jointPositions[1][2], jointPositions[2][2], jointPositions[3][2], jointPositions[4][2], jointPositions[5][2]])

    pyplot.show()
