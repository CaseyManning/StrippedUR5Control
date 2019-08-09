# UR5 Control

## Requirements

Python-urx - `pip3 install urx`
Pygame (only for keyboard control) - `pip3 install pygame`
Firebase - `pip3 install --upgrade firebase-admin`

### Setting up URSim

Download the simulator from [here](https://www.universal-robots.com/download/?option=53321#section41570). Open the RAR file with the Unarchiver Download VMWare, then, then open the .vmx file from the unzipped RAR you downloaded, and the simulator will start. If the simulator then says "No valid peer process to connect to", open system preferences, go to the security and privacy tab, and click `Allow` for URSim. If you are unable to click on anything in URSim, try going into `System Preferences > Security & Privacy > Accessibility` and allow VMWare to control your computer. That should allow you to use the simulator.

Double click on URSim UR5 icon to open it. The simulator will prompt you for safety settings; the default safety settings are ok.

From the menu in the top right menu, go to `Settings > System > Remote Control` and Enable remote control.

Then, go to 'System > Network` and copy down the IP address. 

Create a file titled `config.json` in this directory. Then, add the following line with the IP address from the robot.

`{"ip": "the robot's ip address here"}`

## Viewing in URSim
In the Move section of URSim, select Base under the list Feature (View is currently selected). This ensures that the tool position correlates with the pose of the arm. 

## Connecting to the Robot
Go to Installation > Fieldbus > EtherNet/IP, and Enable.
Go to Settings > System > Network, and select "Static Address". Set the IP address.

If you need to run terminal commands on the robot control tablet, the username is root and the password is easybot.
To get into the terminal, hit ctrl-alt-f1. hit ctrl-alt-f7 to go back to polyscope.

To connect to the robot from your laptop, set the ip in config.json to whatever you set the IP address to, and make sure you are connnected to the same network.

## Installing OnRobot Hand


## Controlling the Robot through Python

## Controlling the Robot Using a Keyboard
The robot can be manipulated through the keyboard by running `arrowKeys.py`. Linear movement is controlled by the arrow keys, '/', and 'shift'. Rotational movement is controlled by WASDQE. Space toggles the state of the gripper between open and closed. 

The movement increment can be changed with ',' and '.', or by pressing 'return' and then inputting the desired increment in your terminal. Optimal fine tuning can be achieved with 0.1-1 mm for linear movements and 5-10 for mrad for rotation.

'J' will print the robot's six joint angles. 'P' will print the TCP's pose. EXCEPT IT DOESN'T FIX IT :).