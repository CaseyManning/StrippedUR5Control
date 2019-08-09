#import urx
import math
from robot import Robot

import urrobot

a = 3 #acceleration
v = 3 #velocity

class CustomRobot(Robot):

    hand = None

    def __init__(self, host, use_rt=True):
        Robot.__init__(self, host, use_rt)

    def _wait_for_move(self, target, threshold=None, timeout=5, joints=False):
        """
        wait for a move to complete. Unfortunately there is no good way to know when a move has finished
        so for every received data from robot we compute a dist equivalent and when it is lower than
        'threshold' we return.
        if threshold is not reached within timeout, an exception is raised
        """
        self.logger.debug("Waiting for move completion using threshold %s and target %s", threshold, target)
        start_dist = self._get_dist(target, joints)
        if threshold is None:
            threshold = start_dist * 0.8
            if threshold < 0.001:  # roboten precision is limited
                threshold = 0.001
            self.logger.debug("No threshold set, setting it to %s", threshold)
        count = 0
        while True:
            dist = self._get_dist(target, joints)
            self.logger.debug("distance to target is: %s, target dist is %s", dist, threshold)
            if not self.secmon.is_program_running():
                if dist < threshold:
                    self.logger.debug("we are threshold(%s) close to target, move has ended", threshold)
                    return
                count += 1
            else:
                count = 0

    def move_relative(self, x, y, z, rx=0, ry=0, rz=0, acc=a, vel=v):
        trans = self.get_pose()  # get current transformation matrix (tool to base)
        trans.pos.x += x
        trans.pos.y += y
        trans.pos.z += z
        trans.orient.rotate_x(rx)
        trans.orient.rotate_y(ry)
        trans.orient.rotate_z(rz)
        # trans.orient.rotate_yb(pi/2)
        self.set_pose(trans, acc=acc, vel=vel, wait=False, command='movel')  # apply the new pose
        self._wait_for_move(trans)

    def move_relativeb(self, x, y, z, rx=0, ry=0, rz=0, acc=a, vel=v):
        trans = self.get_pose()  # get current transformation matrix (tool to base)
        trans.pos.x += x
        trans.pos.y += y
        trans.pos.z += z
        trans.orient.rotate_xb(rx)
        trans.orient.rotate_yb(ry)
        trans.orient.rotate_zb(rz)
        # trans.orient.rotate_yb(pi/2)
        self.set_pose(trans, acc=acc, vel=vel, wait=False, command='movel')  # apply the new pose
        self._wait_for_move(trans)

    def move_absolute(self, x, y, z, rx=0, ry=0, rz=0, acc=a, vel=v):
        target = (x, y, z, rx, ry, rz)
        self.movel(target, acc, vel)
        self._wait_for_move(target)

    def move_absolute_j(self, b, s, e, w1, w2, w3, acc=a, vel=v, degrees=False, wait=True):
        target = (b, s, e, w1, w2, w3)
        if degrees:
            target = tuple([self.d2r(x) for x in target])
        self.movej(target, acc, vel, wait=False)
        if wait:
            self._wait_for_move(target, joints=True)

    def move_absolute_js(self, joint_positions_list, acc=a, vel=v, radius=0.01, degrees=False, wait=True, threshold=None):
        if degrees:
            joint_positions_list = [tuple([self.d2r(x) for x in y]) for y in joint_positions_list]
        self.movexs("movej", joint_positions_list, acc, vel, radius, wait=False)
        print("bob")
        # if wait:
        #     self._wait_for_move(target=joint_positions_list[-1], threshold=threshold, joints=True)
        print("done waiting")




    def d2r(self, x):  # Convert degrees to radians
        return math.radians(x)

    def r2d(self, x):  # Convert radians to degrees
        return math.degrees(x)

    @staticmethod
    def connect(ip):
        robot = CustomRobot(ip)
        return robot