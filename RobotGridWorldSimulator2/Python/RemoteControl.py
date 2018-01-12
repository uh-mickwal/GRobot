#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  RemoteControl.py
#
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
# Version 1.0 Jan 2016
#

# Import the standard Python GUI Library (tkinter)
# Python 2 and 3 compatibility
try:
    # Python 3 tkinter
    import tkinter as tk
except:
    # Else Python 2 Tkinter
    import Tkinter as tk

# Initialise a new GRobot
from grobot import *
robot=NewRobot()

def updateLook():
   global msg 
   msg = str(robot.look())
   lookLabel.config(text=msg)
   
# Create GUI Window
rcApp=tk.Tk()
rcApp.title("GR-Control") # Set Title
global msg
# Create Buttons and place (i.e. pack) into the GUI window
rstButton = tk.Button(rcApp, text="Restart", command=robot.init)
rstButton.pack(side=tk.TOP)
rgtButton = tk.Button(rcApp, text="Right", command=robot.right)
rgtButton.pack(side=tk.RIGHT)
lftButton = tk.Button(rcApp, text="Left", command=robot.left)
lftButton.pack(side=tk.LEFT)
fwButton = tk.Button(rcApp, text="Forward", command=robot.forward)
fwButton.pack()
lookButton=tk.Button(rcApp, text="Look", command=updateLook)
lookButton.pack()
msg = str(robot.look())
lookLabel=tk.Label(rcApp, text=msg)
lookLabel.pack()



    

# Wait for customers!
rcApp.mainloop()
