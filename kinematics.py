    
#!/usr/bin/python2

## UR5/UR10 Inverse Kinematics - Ryan Keating Johns Hopkins University

# from https://github.com/mc-capolei/python-Universal-robot-kinematics/blob/master/universal_robot_kinematics.py

# ***** lib
import numpy as np
from numpy import linalg

import cmath
import math
from math import cos as cos
from math import sin as sin
from math import atan2 as atan2
from math import acos as acos
from math import asin as asin
from math import sqrt as sqrt
from math import pi as pi

global mat
mat=np.matrix

OFFSET = 0.13780008  # offset from base to shoulder in meters

# ****** Coefficients ******

# taken from https://www.universal-robots.com/how-tos-and-faqs/faq/ur-faq/parameters-for-calculations-of-kinematics-and-dynamics-45257/

# d is the link offset
# a is the link length
# alpha is the link twist

# C is just specifying which column of the joint configure matrix "th" you would like to use

global d, a, alph

d = mat([0.1625, 0, 0, 0.1333, 0.0997, 0.0996])
a =mat([0, -0.425, -0.3922, 0, 0, 0])
alph = mat([pi/2, 0, 0, pi/2, -pi/2, 0 ])

def AH(n, th, c):

  T_a = mat(np.identity(4), copy=False)
  T_a[0,3] = a[0,n-1]
  T_d = mat(np.identity(4), copy=False)
  T_d[2,3] = d[0,n-1]

  Rzt = mat([[cos(th[n-1,c]), -sin(th[n-1,c]), 0 ,0],
            [sin(th[n-1,c]),  cos(th[n-1,c]),  0, 0],
            [0,               0,               1, 0],
            [0,               0,               0, 1]],copy=False)
      

  Rxa = mat([[1, 0,           0,                  0],
			 [0, cos(alph[0,n-1]), -sin(alph[0,n-1]),   0],
			 [0, sin(alph[0,n-1]),  cos(alph[0,n-1]),   0],
			 [0, 0,                 0,                  1]],copy=False)

  A_i = T_d * Rzt * T_a * Rxa

  return A_i

def pos(mat):
    return [mat[0, 3], mat[1, 3], mat[2, 3]]

def HTrans(th,c ):  
  A_1=AH(1,th,c)
  A_2=AH(2,th,c)
  A_3=AH(3,th,c)
  A_4=AH(4,th,c)
  A_5=AH(5,th,c)
  A_6=AH(6,th,c)

  offsetVector = OFFSET * np.array([cos(th[0] - pi/2),sin(th[0] - pi/2), 0])

  return [pos(A_1), pos(A_1) + offsetVector, pos(A_1*A_2) + offsetVector, pos(A_1*A_2), pos(A_1*A_2*A_3), pos(A_1*A_2*A_3*A_4), pos(A_1*A_2*A_3*A_4*A_5), pos(A_1*A_2*A_3*A_4*A_5*A_6)]



# angles = mat([[0], [-pi/2], [0], [-pi/2], [0], [0]])
# output = HTrans(angles, [0])
# print()
# print("X: " + str(output[0, 3]) + "\nY: " + str(output[1, 3]) + "\nZ: "+ str(output[2, 3]))
# print()
# ************************************************** INVERSE KINEMATICS 
