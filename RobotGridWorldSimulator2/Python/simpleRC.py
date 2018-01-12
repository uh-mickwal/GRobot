# simpleRC.py
# Simple Remote Control Program for simulated gRobot.
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

robot=NewRobot("robot", colour="yellow")
# You can call your robot any name you want!
# Normal Python variable rules apply (no spaces, chars aA-zZ, etc.)
# Colours can be: “red”, “green”, “blue”, “orange” etc.

msg=""
while msg!="q" and msg!="Q":
        msg = input("Type: F=Forward, R=Turn Right, L = Turn Left. The press RETURN: ")
        if msg == "f" or msg == "F": robot.forward()
        if msg == "l" or msg == "L": robot.left()
        if msg == "r" or msg == "R": robot.right()
        if msg == "i" or msg == "I": robot.init()
exit()
