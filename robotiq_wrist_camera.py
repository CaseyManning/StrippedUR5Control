
from urx.urscript import URScript
import time
import os

boilerplate =  """


  """
class RobotiqWristCameraScript(URScript):
    
    def __init__(self):
        super(RobotiqWristCameraScript, self).__init__()
        # copy the boilerplate to the start of the script to make the RG2() function available
        self.add_line_to_program(boilerplate)

    def _rg2_command(self, target_width=110, target_force=40, payload=0.5, set_payload=False, depth_compensation=False, slave=False):
        self.add_line_to_program("RG2(target_width={}, target_force={}, payload={}, set_payload={}, depth_compensation={}, slave={})"
                                 .format(target_width, target_force, payload, set_payload, depth_compensation, slave))

class RobotiqWristCamera(object):

    def __init__(self, robot):
        self.robot = robot

    def open_gripper(self, target_width=30, target_force=40, payload=0.5, set_payload=False, depth_compensation=False, slave=False, wait=0.5):
        while(self.gripper_position() < 0.5):
            urscript = RobotiqWristCameraScript()
            urscript._rg2_command(target_width, target_force, payload, set_payload, depth_compensation, slave)
            self.robot.send_program(urscript())
            time.sleep(wait)
            if self.gripper_position() < 0.5:
                print('error opening gripper, retrying')

    def gripper_position(self):
        return self.robot.secmon.get_all_data()['ToolData']['analogInput2']
