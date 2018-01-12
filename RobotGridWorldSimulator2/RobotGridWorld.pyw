#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  RoboGridWorld.py
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
# Version 0.1 Sept 2015
# Version 1.0 Nov 2015
# Version 1.1 Jan 2016
#   Fixed (Mac) socket, default map load dir. Contributed by Jamie Hollaway
#   Fixed Bug in Look() routine when robot heading east. MLW
# Version 2  March 2016
#   Fixed serious bug in Look()routine. had to change Map.map file format/size
#       Will load V1 maps, but if saved from V2, will load in V1 program
#       Reccomend update to V2!

# Python 2 and 3 compatibility
from __future__ import absolute_import, division, print_function
try:
      input=raw_input # Python 3 style input()
except:
      pass

try:
    # Python 3 tkinter
    import tkinter as tk
    import tkinter.filedialog as fd
    import tkinter.messagebox as mb

except:
      # Else Python 2 Tkinter
      import Tkinter as tk
      import tkFileDialog as fd
      import tkMessageBox as mb

# Standard imports
from threading import Thread
from time import sleep
import turtle as rbt
import pickle
import socket
import atexit


class GridRobotSim(tk.Tk):
    # Just one big class!
    def __init__(self, master=None):
        self.frmht=622
        self.frmwt=622
        self.gridspace=20
        self.mapsize=30
        self.world=[[None]* (self.mapsize+3) for i in range(self.mapsize+3)]  # World map
        #print(self.world) #debug
        self.robots={} # Mutiple named robots?
        self.shp=[]# Robot shapes list
        self.robotStates={} # Internal states of robots
        self.trails=False # Trails off to start with
        tk.Tk.__init__(self, master)
        tk.Tk.title(self, "RoboGridWorld V2")

        # drawing canvas in frame to include turtle graphics
        self.frame = tk.Frame(master, bg="black", borderwidth=3)
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame,  height = self.frmht, width = self.frmwt, bg="white")
        self.canvas.pack()

        # Buttons under canvas area
        self.newButton=tk.Button(master, text="New Map", command = lambda : self.newWorld())
        self.newButton.pack(side=tk.LEFT)
        self.loadButton=tk.Button(master, text="Load Map", command = lambda : self.loadWorld())
        self.loadButton.pack(side=tk.LEFT)
        self.saveButton=tk.Button(master, text="Save Map", command = lambda : self.saveWorld())
        self.saveButton.pack(side=tk.LEFT)
        self.trailButton=tk.Button(master, text="Toggle Trails", command = lambda : self.toggleTrails())
        self.trailButton.pack(side=tk.RIGHT)
        self.speedSlider=tk.Scale(master,from_=1, to=10, orient=tk.HORIZONTAL, command=self.simSpeed)
        self.speedSlider.set(5)
        self.speedSlider.pack(side=tk.RIGHT)
        self.speedLabel=tk.Label(text="Speed")
        self.speedLabel.pack(side=tk.RIGHT)
        # Add dummy turtle as hidden to set up drawing area
        self.robot1=rbt.RawTurtle(self.canvas) # changes canvas coords! (0,0) now in middle
        self.robot1.hideturtle()
        # Handler for mouse clicks
        self.screen=self.robot1.getscreen()
        self.screen.onclick(self.editGrid, btn=1) # Mouse left button

        self.drawWorld()

        # Start server for robot programs to connect
        self.tcpTrd=Thread(target=self.tcpServer)
        self.tcpTrd.daemon = True
        self.tcpTrd.start()

        # Start timer for simulation speed
        self.timerTrd=Thread(target=self.simtimer)
        self.timerTrd.daemon = True
        self.timerTrd.start()

    def simtimer(self):
        while True:
            self.wait=True
            sleep(0.3-self.delay/50)
            self.wait=False
            sleep(0.05)
            # Bug fix - Jamie Hollaway
            # Stops window freezing when not in focus
            self.update()
            self.update_idletasks()
            #print(self.wait, self.delay)

    def simSpeed(self, event):
        self.delay=self.speedSlider.get()
        #print(self.delay)

    def toggleTrails(self):
        # Work in progress!
        #print("ToggleTrails")# debug
        for robname in self.robots:
            if self.trails == True:
                print("OFF")
                self.robots[robname].penup()
                self.robots[robname].clear()
            else:
                print("ON")
                self.robots[robname].pendown()
        if self.trails==True:
            self.trails=False
        else:
            self.trails=True


    def drawWorld(self):
        # Draws the grid and labels
        # XYaxis lines, labels
        # Vertical lines
        self.canvas.delete("all")
        count=0
        for i in range(-self.frmht//2, self.frmht//2-1, self.gridspace ):
                self.canvas.create_line(i, self.frmht//2, i, -self.frmwt//2, dash=(2,4))
                self.canvas.create_text(i+10, self.frmht//2-10, text=str(count), font=("courier", 6), fill="red")
                count += 1
        # Horizontal lines
        count=self.frmht//self.gridspace
        for i in range(-self.frmwt//2, self.frmwt//2-1,self.gridspace ):
                self.canvas.create_line(-self.frmwt//2,i, self.frmht//2, i, dash=(2,4))
                self.canvas.create_text(-self.frmwt//2+10, i+12, text=str(int(count-1)), font=("courier", 6), fill="red")
                count -= 1

        # Set boundary walls: 0,0 to 31,31
        mapsize = len(self.world)-1
        #print(mapsize) # debug
        for n in range(0,mapsize ):
            self.world[0][n]="Wall"
            self.world[mapsize][n]="Wall"
            self.world[n][0]="Wall"
            self.world[n][mapsize]="Wall"
        self.world[mapsize][mapsize] = "Wall"

        # Draw filled grids squares
        #print ("World dims = ", len(self.world), len(self.world[0]))#debug
        for ix in range(0,len(self.world)-1):
            for iy in range(0,len(self.world[ix])-1):
                if self.world[ix+1][iy+1] != None:
                    #print(ix, iy, self.world[ix][iy])# debug
                    self.fillGrid(ix, iy)
                else:
                    self.clearGrid(ix,iy)


    def editGrid(self, mousex, mousey):
        x=self.maptoX(mousex)
        y=self.maptoY(mousey)
        #print("EditGrid", mousex, mousey, x, y, self.world[x][y])# Debug
        if self.world[x+1][y+1] == None:
            # Make wall (etc.?)
            self.fillGrid(x, y)
            self.world[x+1][y+1] = "Wall"
        else: #Clear grid square
            self.clearGrid(x, y)
            self.world[x+1][y+1] = None

    def fillGrid(self, x, y):
        tagstr=[str(x)+"u"+str(y), "walls"]
        #print("**"+tagstr+"**", self.world[x+1][y+1]) # debug
        self.canvas.create_line(self.xtoMap(x)-11, self.ytoMap(y),
                                self.xtoMap(x)+8, self.ytoMap(y),
                                 fill="grey", width=19, tag=tagstr)

    def clearGrid(self, x, y):
        tagstr=str(x)+"u"+str(y)
        self.canvas.delete(tagstr)

    def xtoMap(self, x=0):
        return int(-self.frmwt//2 + 12 + x * self.gridspace)

    def ytoMap(self, y=0):
        return int(self.frmwt//2 - 12 - y * self.gridspace)

    def maptoX (self, mapx=0):
        return int((mapx + self.frmwt//2) // self.gridspace)

    def maptoY(self, mapy=0):
        return int(self.mapsize - (mapy - self.frmht//2 ) // -self.gridspace)

    def newWorld(self):
        # print("NewMAp")
        self.world=[[None]* (self.mapsize+3) for i in range(self.mapsize+3)]  # World map
        self.drawWorld()

    def saveWorld(self):
        # print("SaveMAp")
        filename = fd.asksaveasfilename(filetypes=[("Map Files","*.map")], initialdir=".")
        if filename != None:
            # remove robots from world!
            for robname in list(self.robots.keys()):
                xpos,ypos=self.getXYpos(robname)
                self.world[xpos+1][ypos+1]=None
            # Then save!
            if filename[-4:] != ".map": filename += ".map"
            pickle.dump(self.world, open(filename, 'wb'),2) # Protocol 2 for python 2 compatilbility

    def loadWorld(self):
        filename=fd.askopenfilename(filetypes=[("Map Files","*.map")], initialdir="./Maps/")
        #print(filename)# debug
        if filename != "":
            if filename[-4:] != ".map": filename += ".map"
            newworld=pickle.load(open(filename, 'rb'))
            if len(newworld)<32: # Old style or part map
                # map onto new style map
                #print("Old Style Map")
                self.world=[[None]* (self.mapsize+3) for i in range(self.mapsize+3)]  # Clear World map
                dx = 1
                for ix in newworld:
                    dy=1
                    for iy in ix:
                        #print(dx, dy)#debug
                        self.world[dx][dy] = iy
                        dy += 1
                    dx +=1
            else:
                #print("New Style Map")#debug
                self.world = newworld
            self.drawWorld()

    def newRobot(self, robname="None",  posx=1, posy=1, colour="red", rshape="None"):
        if robname == "None":
            # create/use Anonymous robot. Can only do one!
            robname = "anon"
        if not robname in self.robots:
            self.robots[robname]=rbt.RawTurtle(self.canvas)
        else:
            # Remove "old" robot from World
           self.world[self.maptoX(self.robots[robname].xcor())+1] [self.maptoY(self.robots[robname].ycor())+1] = None
        # Robot shape/colour
        if rshape == "None": # Can provide own shape def
            # Otherwise use standard robot shape
            self.shp.append(rbt.Shape("compound"))
            #print(self.shp, len(self.shp)-1)# debug
            poly1 = ((0,0),(10,-5),(0,10),(-10,-5))
            self.shp[len(self.shp)-1].addcomponent(poly1, colour, "black")
            poly2 = ((0,0),(10,-5),(-10,-5))
            self.shp[len(self.shp)-1].addcomponent(poly2, "black", colour)
            self.screen.register_shape(robname+"shape", self.shp[len(self.shp)-1])
        else:
            # Can use standard shape  “arrow”, “turtle”, “circle”,
            # “square”, “triangle”, “classic”
            self.robots[robname].shape(rshape)
        # Initalise robot
        self.robotStates[robname]=0
        self.robots[robname].hideturtle()
        self.robots[robname].pencolor(colour)
        self.robots[robname].clear()
        self.robots[robname].penup()
        self.robots[robname].shape(robname+"shape")
        self.robots[robname].speed(0)
        self.robots[robname].goto(self.xtoMap(posx)-3, self.ytoMap(self.mapsize-posy)+2)
        self.robots[robname].setheading(90)
        self.robots[robname].showturtle()
        if self.trails == True:
            self.robots[robname].clear()
            self.robots[robname].pendown()
        else:
            self.robots[robname].penup()
            self.robots[robname].clear()
        self.robots[robname].speed(2)
        self.world[posx+1][posy+1]=robname
        return "OK"

    def getXYpos(self, robname):
        posx = self.maptoX(self.robots[robname].xcor())
        posy = self.maptoY(self.robots[robname].ycor())
        return (posx, posy)

    def moveForward(self, rname):
        if rname in self.robots and self.robotStates[rname]!="Broken":
            if self.look(rname)[2]==None:# Clear to move
                posx = self.maptoX(self.robots[rname].xcor())
                posy = self.maptoY(self.robots[rname].ycor())

                self.world[posx+1][posy+1]=None # Clear robot from world
                self.robots[rname].forward(20) # move to next grid square
                posx = self.maptoX(self.robots[rname].xcor())
                posy = self.maptoY(self.robots[rname].ycor())
                self.world[posx+1][posy+1]=rname # update to world to show robot
                return "OK"
            else:
                # If not clear (None), then collision
                self.robots[rname].shape("circle")
                self.robotStates[rname]="Broken" # Out of order!
                return "Bang"
        elif self.robotStates[rname]!="Broken":
            return "Broken"
        else:
            return "Error"

    def turnLeft(self, rname):
        if rname in self.robots:
            if self.robotStates[rname]!="Broken":
                self.robots[rname].left(90)
                return "OK"
            else:
                return "Broken"
        return "Robot name not found"

    def turnRight(self, rname):
        if rname in self.robots:
            if self.robotStates[rname]!="Broken":
                self.robots[rname].right(90)
                return "OK"
            else:
                return "Broken"
        return "Robot name not found"

    def look(self, rname):
        if rname in self.robots :
            if self.robotStates[rname]!="Broken":
                posx = self.maptoX(self.robots[rname].xcor())
                posy = self.maptoY(self.robots[rname].ycor())
                heading=int(self.robots[rname].heading())
                #print(rname, posx, posy, heading) # debug

                if heading == 0 and posx <31: #East
                    val = [self.world[posx+1][posy+2],self.world[posx+2][posy+2],
                        self.world[posx+2][posy+1], self.world[posx+2][posy], self.world[posx+1][posy]]
                elif heading == 90 and posy <31: #North
                    val = [self.world[posx][posy+1], self.world[posx][posy+2],
                        self.world[posx+1][posy+2], self.world[posx+2][posy+2], self.world[posx+2][posy+1]]
                elif heading == 180 and posx >= 0: #West
                    val = [self.world[posx+1][posy],self.world[posx][posy],
                        self.world[posx][posy+1], self.world[posx][posy+2],self.world[posx+1][posy+2]]
                elif heading == 270 and posy >= 0:# South
                    val = [self.world[posx+2][posy+1], self.world[posx+2][posy],
                        self.world[posx+1][posy], self.world[posx][posy], self.world[posx][posy+1]]
                else:
                    #print("Edge of world")#debug
                    # Facing edge of world
                    val==["Wall", "Wall", "Wall", "Wall", "Wall"]
                    """
                    if heading == 0: #East edge
                        if posy<30: #Not upper right corner
                            val[0] = self.world[posx][posy+1]
                        elif posy>0: # Not lower left corner
                            val[4] = self.world[posx][posy-1]

                    elif heading == 180:# West edge
                        if posy<30: # Not Upper Right corner
                            val[4] = self.world[posx][posy+1]
                        elif posy>0: # Not Lower rightcorner
                            val[0] = self.world[posx][posy-1]

                    elif heading == 90: #North edge
                        if posx<30: # Not Upper Right corner
                            val[4] = self.world[posx+1][posy]
                        elif posx>0: # Not Upper Left Corner
                            val[0] = self.world[posx-1][posy]

                    else: # South edge
                        if posx<30: #Not lower left corner
                            val[0] = self.world[posx+1][posy]
                        elif posx>0: # Not lower right corner
                            val[4] = self.world[posx-1][posy]
                    """
                #print("world val = ", val)# debug
                #if val == None: val = "None"
                return val
            else:
                return ["Broken", "Broken", "Broken", "Broken", "Broken"]
        return "Robot name not found"


    def tcpServer(self):
        """
        TCIP server, opens a TC IP socket and passes the message on to be executed and
        waits for input from the TCIP socket and pases it on to despatch() for
        evaluation. If "q" input, ends connection, "Q" input ends server.
        """
        #variables
        msg = ""
        rmsg = ""
        passw=""
        tcpSock=None
        tcpOk=0
        try:
            # Create IP socket and wait for customers
            tcpSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print("Error creating socket")
        print("Please wait: Binding address to socket")
        # Bug fix for Mac - C ontributed by Jamie Hollaway
        tcpSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        msgtext=tk.Label(self.frame, text="Please Wait: Setting up Connection", bg="red")
        msgtext.pack(side=tk.TOP)
        while tcpOk==0:
            try:
                tcpSock.bind(("localhost",9001))
                tcpSock.listen(3)
                tcpOk=1
            except:
                sleep(1.0) # Keep trying!
        print("Socket ready now")
        msgtext.destroy()
        #make sure socket closes at eop
        atexit.register(tcpSock.close)
        atexit.register(tcpSock.shutdown, 1)
        msg=""
        while tcpOk==1:
            # when customer calls, service requests
            cli_sock, cli_ipAdd = tcpSock.accept()
            try:
                # python 3
                thrd=Thread(target = self.despatch, args = (cli_sock,))
                thrd.daemon = True
                thrd.start()
            except:
                #raise # debug
                print("Warning TCP/IP Error") # Just keep on with next request
        # Clean up if this point ever reached
        tcpSock.shutdown(1)
        tcpSock.close()
        print("Server closed")


    def despatch(self, cli_sock):
        msg = ""
        rmsg = ""
        # Recive input and pass to eval
        # print("Connected") # Debug
        msg=cli_sock.recv(50).decode('utf-8')
        print("*"+msg)#debug
        if (msg != "Q"):
            msg = msg.split() # parse
            #for i in msg: print(i) #debug

            # Do robot commands
            try:
                if msg[0]=="N":
                    #print(msg) #debug
                    # New or init robot
                    rmsg = self.newRobot(msg[1], int(msg[2]), int(msg[3]), msg[4], msg[5])
                elif msg[0]=="F":
                    # msg[1] is robot name
                    rmsg = self.moveForward(msg[1])
                elif msg[0]=="R":
                    rmsg = self.turnRight(msg[1])
                elif msg[0]=="L":
                    rmsg = self.turnLeft(msg[1])
                elif msg[0] == "S":
                    rmsg = str(self.look(msg[1]))
                elif msg[0]=="P":
                    rmsg = self.getXYpos(msg[1])
                else:
                    rmsg="Unknown command"
            except:
                #raise #debug. If error just carry on
                rmsg = "Server Error"

            if rmsg == None:
                rmsg == "None"
            #print(rmsg, type(rmsg))# debug
            # Wait here for step timer
            while self.wait==True:
                sleep(0.01)
            cli_sock.send(str(rmsg).encode('utf-8'))
        #print("Connection Closed")# debug
        cli_sock.close()
        return

if __name__ == '__main__':
    GRSApp = GridRobotSim()
    GRSApp.mainloop()


