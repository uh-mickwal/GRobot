# mazeSolve.py
# Left Hand Rule, maze solving Program for simulated gRobot.
# M L Walters, Version 1.0 Feb 2016

# Python 2 and 3 compatibility. Use Python 3 syntax
from __future__ import absolute_import, division, print_function
try:
      input=raw_input # Python 3 style input()
except:
      pass

# You can use the demo map file "Maze.map", or create your own by
# mouse clicking on the map area to raise/lower walls.

# Initialise a new GRobot
from grobot import *
robot=NewRobot("robot", colour="blue")

msg=[] # Create an empty list to receive robot.look() data
print ("Press Ctrl C to Stop")


while True:
        try:
                msg = robot.look()
                #input("Press RETURN to cont.")
                if msg[4] == None:
                        robot.right()
                        robot.forward()
                elif msg[2] == None:
                        robot.forward()
                else:
                        robot.left()
        except KeyboardInterrupt:
                break
exit()
