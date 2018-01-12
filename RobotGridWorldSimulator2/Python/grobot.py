#! /usr/bin/python3
#  Copyright 2015 Mick Walters <Mick Walters> M.L.Walters@herts.ac.uk
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# Version 0.1 Sept 2015
# Version 1.0 Nov 2015
# Version 1.1 Jan 2016 - Fixed socket bug, contributed by Jamie Hollaway
#
"""
grobot.py - A client API for the RobotGridWorld Simulator
M L Walters. V0.5 Nov 2015
M L Walters, V1.0 Nov 2015
M L Walters, V1.2 Dec 2015

Note, this module (grobot.py program file) must either be placed in the current
working directory (folder) or in a suitable directory in the Python standard
search path.

When imported into your own robot control program, grobot.py provides a simple
Application Programming Interface (API) for the RobotGridWorld.py Robot
Simulator. This must be already running when you run your grobot program
otherwise an error message will be displayed, and your grobot program will
terminate.

******************************
RobotGridWorld Robot Simulator
******************************

To run the simulator, simply double click on the program icon from your
favourite file manager (Linux) or File Explorer (Windows or Mac).

The simulator program will intially display a blank map, which is a 30x30 grid,
with x and y co-ordinates marked along the lower and left sides respectively.
There are several buttons availalble categorised as:

Map Editing Controls:
    "New Map"   - Clears the current Map ready for editng a new one
    "Load Map"  - Loads a previously saved map
    "Save Map"  - Saves the current (edited) map, for later loading

Clicking anywhere on the map grid area will toggle the building and removal of
walls  on the map. When the pattern of walls is as required, the map can be
saved (click "Save Map" to a file (extension <name>.map). The edited map can be
recalled by selecting "Load Map".

Simulation Controls:
"Toggle Trails" - Toggles the display of pproriately coloured trials for each robot
"Speed"         - A slider control to adjusts the speed of the simulated robot(s)
                  movements.

***************************************
Creating RobotGrid World Robot Programs
***************************************

At the beginning of your robot program, you must first import the grobot.py
clientinto your own program. Usage:

import grobot

To create a new robot in the simulated world, use:

robotname=grobot.NewRobot(<name>, <xpos>, <ypos>, <colour>, <shape>)

Where:
    <name> is a string which contains the name of the robot. If several
    robots e]used, all must have unique names.

    Integers <xpos> and <ypos> (both between 0 and 31) are the initial or
    starting world co-ordinate position of the robot. If left blank, the
    robot will be set to starting position x = 1, Y = 1.

    <colour> is a string which denotes which colour the robot will be.
    The common colours are ; "red", "blue", "green", "yellow", "black".
    If the parameter is not provided, the robot will be red.

    <shape> is a string that denotes one of the standard turtle shapes. Left
    blank or None if the standard robot shape is to be used
    See the Python Turtle doc for details.

The parameters for this function are all optional, but if several robots are to
be simulated simutaneously, the <name> parameter must be supplied, and the
initial positions (xpos, and ypos) must be different. E.g.:

fred = grobot.NewRobot("fred", 1, 2, "blue")

If the simulator is not running, an error message will be
displayed, and the program will exit.

Once a robot is created (instantiated), the robot object has five methods
available. E.g. if the robot is instantiated as fred:

    fred.forward() # Moves robot orthogonally forward one grid square.
                   # If way is blocked returns "Bang" and the robot will turn
                   # into a black circle, otherwise returns "OK"
                   # If the robot has already returned "Bang", subsequent calls to
                   # forward will return "Broken"
    fred.right()   # robot turns 90 degrees right, returns "OK", or "Broken" if a
                   # collision has occured
    fred.left()    # robot turns 90 degrees left, returns "OK", or "Broken" if a
                   # collision has occured
    fred.look()    # Returns a list of elements [viewLeft, viewDiagLeft,
                   # viewForward, viewDiagRight, viewRight]
                   # Each element can be either "Wall" if the forward way
                   # is blocked by a Wall, a name of the robot
                   # blocking the way, or None if the way is clear. If a collison
                   # has occured, this will return a list of ["Broken"]*5.
    fred.init(x,y) # Resets and initialises the named robot to start position
                   # (x, y). Note. x and y are optional. If left out uses last
                   # provided values from an init() or NewRobot

There is one function in the module availalble: grobot.demo()
This provides a short demo of how to create a NewRobot() and use the
methods described above. The demo is run automatically if the module is
run directly (i.e. not imported):

def demo():
    # print used to show return value from method/function calls
    fred=NewRobot("fred", 1, 1)
    bill=NewRobot("bill", 1, 1, "green")
    print("Fred forward", fred.forward())
    print("Bill forward",bill.forward())
    print("Fred right", fred.right())
    print("Bill right", bill.right())
    #fred.init(7,7)
    count = 12
    while count > 0:
        #print(count)
        print("Fred looks at:", fred.look())
        print("Fred forward",fred.forward())
        print("Bill looks at:", bill.look())
        print ("Bill forward",bill.forward())
        count -= 1

    print("Fred looks forward at", fred.look()[2]) # element 2 is forward view
    print("Bill looks forward at", bill.look()[2])


Note, if you load either the "Demo.map" or Test.map world into tthe simulator,
the grobot.demo() will demonstrate the options and return values from the robot
methods (functions). You can also import and use the grobot module (program)
from the interactive shell and try out the commands interactively, e.g.:

>>>import grobot
>>>grobot.demo()
>>>fred = grobot.NewRobot("fred", 5, 5, "red")
>>>fred.look()
"wall"
>>>fred.forward()
"Bang"
>>>fred.init()
"OK"
>>>

You can also display this guide by using Python's interactive help function:

>>>help("grobot")

"""
# Python 2 and 3 compatibility
from __future__ import absolute_import, division, print_function
try:
      input=raw_input # Python 3 style input()
except:
      pass

import socket
from time import sleep
import atexit
import sys

hostname="localhost" # Set to Tutors PC IP address to shown on Projector etc?
port = 9001          # Possibility of various clients running own robots
                     # in the simulator in future?


class NewRobot():

    def __init__(self, rname="anon", posx=1, posy=1, colour="red", rshape="None"):
        self.rname=rname
        self.posx=posx
        self.posy=posy
        self.colour=colour
        self.rshape=rshape
        msg = "N "+str(rname)+" "+str(posx)+" "+str(posy)+" "+colour+" "+rshape
        #print(msg)
        self._send(msg)
        #atexit.register(self.tcpSock.close)
        #atexit.register(self.tcpSock.shutdown, 1)

    def _send(self, msg):
        # Send message and get respose from Simulator
        try:
            # The simulator IP is on localhost, maybe to remote PC later?
            if type(msg)==str:
                #self.tcpSock.setblocking(0)
                self.tcpSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Repeated runs can sometimes hang up here, because
                # the socket hasn't been released by the kernel
                # So this tells the socket to reuse the old one if it exists
                self.tcpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.tcpSock.connect ((hostname, port))# (hostname,portno))
                self.tcpSock.send(msg.encode('utf-8'))

                tries=1
                rmsg=""
                while rmsg=="" and tries > 0:
                    rmsg = rmsg + self.tcpSock.recv(100).decode('utf-8')
                    if rmsg!="":tries -= 1
                self.tcpSock.close()
            else:
                rmsg = "msg type error"
            if rmsg == "": rmsg = "Warning: Receieved Data error"
        except:
            print("Cannot connect to simulator")
            print("Please make sure Simulator is running")
            exit()

        #self.tcpSock.shutdown(socket.SHUT_RDWR)
        #self.tcpSock.close()
        #print(rmsg)# Debug
        return rmsg

    def init(self, xpos=1, ypos=1):
        self.xpos=xpos
        self.ypos=ypos
        return self._send("N " + self.rname+" "+str(self.xpos)+" "+str(self.ypos)+" "+self.colour+" "+ self.rshape)

    def right(self):
        return self._send("R "+ self.rname+" ")

    def left(self):
        return self._send("L " + self.rname+" ")

    def look(self):
        
        ##return 
         #eval(
        msg = self._send("S " + self.rname)
        print(msg)
        return eval(msg)

    def forward(self):
        return self._send("F " + self.rname)



def demo():
    # print() used to show return value from method/function calls
    fred=NewRobot("fred", 1, 1)
    bill=NewRobot("bill", 1, 1, "green")
    print("Fred forward", fred.forward())
    print("Bill forward",bill.forward())
    print("Fred right", fred.right())
    print("Bill right", bill.right())
    #fred.init(7,7)
    count = 12
    while count > 0:
        #print(count)
        print("Fred looks at:", fred.look())
        print("Fred forward",fred.forward())
        print("Bill looks at:", bill.look())
        print ("Bill forward",bill.forward())
        count -= 1
    print("Fred looks forward at", fred.look()[2])
    print("Bill looks forward at", bill.look()[2])

def demo2():
    arthur=NewRobot("arthur", 1, 4, "blue")
    ted=NewRobot("ted", 4, 4, "yellow")
    print("Arthur forward", arthur.forward())
    print("Ted forward",ted.forward())
    print("Arthur right", arthur.right())
    print("Ted right", ted.right())
    count = 12
    while count > 0:
        #print(count)
        print("Arthur looks at: ", arthur.look())
        print("Arthur forward",arthur.forward())
        print("Ted looks at:", ted.look())
        print ("Ted forward",ted.forward())
        count -= 1
    print("Arthur looks at:", arthur.look())
    print("ted looks at:", ted.look())

if __name__ == "__main__":
    demo()
    print("Finished")

