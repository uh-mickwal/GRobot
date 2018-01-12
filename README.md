# GRobot

A simple grid world based simulated robot written in pure Python, using only standard libs and Python 2 and 3 compatible.
 
# RobotGridWorldSimulator.pyw - A simple grid world based simulated robot written in pure Python, using only standard libs and Python 2 and 3 compatible.and Python 2 and 3 compatible.

# GRobot.py - A client API for the RobotGridWorld Simulator M L Walters. V0.5 Nov 2015 M L Walters, V1.0 Nov 2015 M L Walters, V1.2 Dec 2015, V2.1 Feb 2016

Note, this module (grobot.py program file) must either be placed in the current working directory (folder) or in a suitable directory in the Python standard search path.

When imported into your own robot control program, grobot.py provides a simple Application Programming Interface (API) for the RobotGridWorld.py Robot Simulator. This must be already running when you run your grobot program otherwise an error message will be displayed, and your grobot program will terminate.

RobotGridWorld Robot Simulator

To run the simulator, simply double click on the program icon from your favourite file manager (Linux) or File Explorer (Windows or Mac).

The simulator program will intially display a blank map, which is a 30x30 grid, with x and y co-ordinates marked along the lower and left sides respectively. There are several buttons availalble categorised as:

Map Editing Controls: "New Map" - Clears the current Map ready for editng a new one "Load Map" - Loads a previously saved map "Save Map" - Saves the current (edited) map, for later loading

Clicking anywhere on the map grid area will toggle the building and removal of walls on the map. When the pattern of walls is as required, the map can be saved (click "Save Map" to a file (extension .map). The edited map can be recalled by selecting "Load Map".

Simulation Controls: "Toggle Trails" - Toggles the display of pproriately coloured trials for each robot "Speed" - A slider control to adjusts the speed of the simulated robot(s) movements.

Creating RobotGrid World Robot Programs

At the beginning of your robot program, you must first import the grobot.py clientinto your own program. Usage:

import grobot

To create a new robot in the simulated world, use:

robotname=grobot.NewRobot(, , , , )

Where: is a string which contains the name of the robot. If several robots e]used, all must have unique names.

Integers and (both between 0 and 31) are the initial or starting world co-ordinate position of the robot. If left blank, the robot will be set to starting position x = 1, Y = 1.

is a string which denotes which colour the robot will be. The common colours are ; "red", "blue", "green", "yellow", "black". If the parameter is not provided, the robot will be red.

is a string that denotes one of the standard turtle shapes. Left blank or None if the standard robot shape is to be used See the Python Turtle doc for details.

The parameters for this function are all optional, but if several robots are to be simulated simutaneously, the parameter must be supplied, and the initial positions (xpos, and ypos) must be different. E.g.:

fred = grobot.NewRobot("fred", 1, 2, "blue")

If the simulator is not running, an error message will be displayed, and the program will exit.

Once a robot is created (instantiated), the robot object has five methods available. E.g. if the robot is instantiated as fred:

fred.forward() # Moves robot orthogonally forward one grid square. # If way is blocked returns "Bang" and the robot will turn # into a black circle, otherwise returns "OK" # If the robot has already returned "Bang", subsequent calls to # forward will return "Broken" fred.right() # robot turns 90 degrees right, returns "OK", or "Broken" if a # collision has occured fred.left() # robot turns 90 degrees left, returns "OK", or "Broken" if a # collision has occured fred.look() # Returns a list of elements [viewLeft, viewDiagLeft, # viewForward, viewDiagRight, viewRight] # Each element can be either "Wall" if the forward way # is blocked by a Wall, a name of the robot # blocking the way, or None if the way is clear. If a collison # has occured, this will return a list of ["Broken"]*5. fred.init(x,y) # Resets and initialises the named robot to start position # (x, y). Note. x and y are optional. If left out uses last # provided values from an init() or NewRobot

There is one function in the module availalble: grobot.demo() This provides a short demo of how to create a NewRobot() and use the methods described above. The demo is run automatically if the module is run directly (i.e. not imported):

def demo(): # print used to show return value from method/function calls fred=NewRobot("fred", 1, 1) bill=NewRobot("bill", 1, 1, "green") print("Fred forward", fred.forward()) print("Bill forward",bill.forward()) print("Fred right", fred.right()) print("Bill right", bill.right()) #fred.init(7,7) count = 12 while count > 0: #print(count) print("Fred looks at:", fred.look()) print("Fred forward",fred.forward()) print("Bill looks at:", bill.look()) print ("Bill forward",bill.forward()) count -= 1

print("Fred looks forward at", fred.look()[2]) # element 2 is forward view print("Bill looks forward at", bill.look()[2])

Note, if you load either the "Demo.map" or Test.map world into tthe simulator, the grobot.demo() will demonstrate the options and return values from the robot methods (functions). You can also import and use the grobot module (program) from the interactive shell and try out the commands interactively, e.g.:

        import grobot grobot.demo() fred = grobot.NewRobot("fred", 5, 5, "red") fred.look() "wall" fred.forward() "Bang" fred.init() "OK"
# GRobot

# RobotGridWorldSimulator.pyw - A simple grid world based simulated robot written in pure Python, using only standard libs and Python 2 and 3 compatible.

# grobot.py - A client API lib for the RobotGridWorld Simulator 
# M L Walters, V1.2 Dec 2015

Note, the module (grobot.py program file) must either be placed in the current working directory (folder) or in a suitable directory in the Python standard search path.

When imported into your own robot control program, grobot.py provides a simple Application Programming Interface (API) for the RobotGridWorld.py Robot Simulator which must be already running when you run your gRobot program otherwise an error message will be displayed, and your gRobot program will terminate.

RobotGridWorld Robot Simulator

To run the simulator, simply double click on the program icon from your favourite file manager (Linux) or File Explorer (Windows or Mac).

The simulator program will intially display a blank map, which is a 30x30 grid, with x and y co-ordinates marked along the lower and left sides respectively. There are several buttons availalble categorised as:

Map Editing Controls: "New Map" - Clears the current Map ready for editng a new one "Load Map" - Loads a previously saved map "Save Map" - Saves the current (edited) map, for later loading

Clicking anywhere on the map grid area will toggle the building and removal of walls on the map. When the pattern of walls is as required, the map can be saved (click "Save Map" to a file (extension .map). The edited map can be recalled by selecting "Load Map".

Simulation Controls: "Toggle Trails" - Toggles the display of pproriately coloured trials for each robot "Speed" - A slider control to adjusts the speed of the simulated robot(s) movements.

Creating RobotGrid World Robot Programs

At the beginning of your robot program, you must first import the grobot.py clientinto your own program. Usage:

import grobot

To create a new robot in the simulated world, use:

robotname=grobot.NewRobot()

Where: is a string which contains the name of the robot. If several robots e]used, all must have unique names.

Integers and (both between 0 and 31) are the initial or starting world co-ordinate position of the robot. If left blank, the robot will be set to starting position x = 1, Y = 1.

is a string which denotes which colour the robot will be. The common colours are ; "red", "blue", "green", "yellow", "black". If the parameter is not provided, the robot will be red.

is a string that denotes one of the standard turtle shapes. Left blank or None if the standard robot shape is to be used See the Python Turtle doc for details.

The parameters for this function are all optional, but if several robots are to be simulated simutaneously, the parameter must be supplied, and the initial positions (xpos, and ypos) must be different. E.g.:

fred = grobot.NewRobot("fred", 1, 2, "blue")

If the simulator is not running, an error message will be displayed, and the program will exit.and Python 2 and 3 compatible.

GRobot.py - A client API for the RobotGridWorld Simulator M L Walters. V0.5 Nov 2015 M L Walters, V1.0 Nov 2015 M L Walters, V1.2 Dec 2015

Note, this module (grobot.py program file) must either be placed in the current working directory (folder) or in a suitable directory in the Python standard search path.

When imported into your own robot control program, grobot.py provides a simple Application Programming Interface (API) for the RobotGridWorld.py Robot Simulator. This must be already running when you run your grobot program otherwise an error message will be displayed, and your grobot program will terminate.

RobotGridWorld Robot Simulator

To run the simulator, simply double click on the program icon from your favourite file manager (Linux) or File Explorer (Windows or Mac).

The simulator program will intially display a blank map, which is a 30x30 grid, with x and y co-ordinates marked along the lower and left sides respectively. There are several buttons availalble categorised as:

Map Editing Controls: "New Map" - Clears the current Map ready for editng a new one "Load Map" - Loads a previously saved map "Save Map" - Saves the current (edited) map, for later loading

Clicking anywhere on the map grid area will toggle the building and removal of walls on the map. When the pattern of walls is as required, the map can be saved (click "Save Map" to a file (extension .map). The edited map can be recalled by selecting "Load Map".

Simulation Controls: "Toggle Trails" - Toggles the display of pproriately coloured trials for each robot "Speed" - A slider control to adjusts the speed of the simulated robot(s) movements.

Creating RobotGrid World Robot Programs

At the beginning of your robot program, you must first import the grobot.py clientinto your own program. Usage:

import grobot

To create a new robot in the simulated world, use:

robotname=grobot.NewRobot()

Where: is a string which contains the name of the robot. If several robots e]used, all must have unique names.

Integers and (both between 0 and 31) are the initial or starting world co-ordinate position of the robot. If left blank, the robot will be set to starting position x = 1, Y = 1.

is a string which denotes which colour the robot will be. The common colours are ; "red", "blue", "green", "yellow", "black". If the parameter is not provided, the robot will be red.

is a string that denotes one of the standard turtle shapes. Left blank or None if the standard robot shape is to be used See the Python Turtle doc for details.

The parameters for this function are all optional, but if several robots are to be simulated simutaneously, the parameter must be supplied, and the initial positions (xpos, and ypos) must be different. E.g.:

fred = grobot.NewRobot("fred", 1, 2, "blue")

If the simulator is not running, an error message will be displayed, and the program will exit.

Once a robot is created (instantiated), the robot object has five methods available. E.g. if the robot is instantiated as fred:

fred.forward() # Moves robot orthogonally forward one grid square. # If way is blocked returns "Bang" and the robot will turn # into a black circle, otherwise returns "OK" # If the robot has already returned "Bang", subsequent calls to # forward will return "Broken" fred.right() # robot turns 90 degrees right, returns "OK", or "Broken" if a # collision has occured fred.left() # robot turns 90 degrees left, returns "OK", or "Broken" if a # collision has occured fred.look() # Returns a list of elements [viewLeft, viewDiagLeft, # viewForward, viewDiagRight, viewRight] # Each element can be either "Wall" if the forward way # is blocked by a Wall, a name of the robot # blocking the way, or None if the way is clear. If a collison # has occured, this will return a list of ["Broken"]*5. fred.init(x,y) # Resets and initialises the named robot to start position # (x, y). Note. x and y are optional. If left out uses last # provided values from an init() or NewRobot

There is one function in the module availalble: grobot.demo() This provides a short demo of how to create a NewRobot() and use the methods described above. The demo is run automatically if the module is run directly (i.e. not imported):

def demo(): # print used to show return value from method/function calls fred=NewRobot("fred", 1, 1) bill=NewRobot("bill", 1, 1, "green") print("Fred forward", fred.forward()) print("Bill forward",bill.forward()) print("Fred right", fred.right()) print("Bill right", bill.right()) #fred.init(7,7) count = 12 while count > 0: #print(count) print("Fred looks at:", fred.look()) print("Fred forward",fred.forward()) print("Bill looks at:", bill.look()) print ("Bill forward",bill.forward()) count -= 1

print("Fred looks forward at", fred.look()[2]) # element 2 is forward view print("Bill looks forward at", bill.look()[2])

Note, if you load either the "Demo.map" or Test.map world into tthe simulator, the grobot.demo() will demonstrate the options and return values from the robot methods (functions). You can also import and use the grobot module (program) from the interactive shell and try out the commands interactively, e.g.:

        import grobot grobot.demo() 
        fred = grobot.NewRobot("fred", 5, 5, "red") 
        fred.look() -> "wall" 
        fred.forward() "Bang" fred.init() ->  "OK"


Once a robot is created (instantiated), the robot object has five methods available. E.g. if the robot is instantiated as fred:

fred.forward() # Moves robot orthogonally forward one grid square. # If way is blocked returns "Bang" and the robot will turn # into a black circle, otherwise returns "OK" # If the robot has already returned "Bang", subsequent calls to # forward will return "Broken" fred.right() # robot turns 90 degrees right, returns "OK", or "Broken" if a # collision has occured fred.left() # robot turns 90 degrees left, returns "OK", or "Broken" if a # collision has occured fred.look() # Returns a list of elements [viewLeft, viewDiagLeft, # viewForward, viewDiagRight, viewRight] # Each element can be either "Wall" if the forward way # is blocked by a Wall, a name of the robot # blocking the way, or None if the way is clear. If a collison # has occured, this will return a list of ["Broken"]*5. fred.init(x,y) # Resets and initialises the named robot to start position # (x, y). Note. x and y are optional. If left out uses last # provided values from an init() or NewRobot

There is one function in the module availalble: grobot.demo() This provides a short demo of how to create a NewRobot() and use the methods described above. The demo is run automatically if the module is run directly (i.e. not imported):

def demo(): # print used to show return value from method/function calls fred=NewRobot("fred", 1, 1) bill=NewRobot("bill", 1, 1, "green") print("Fred forward", fred.forward()) print("Bill forward",bill.forward()) print("Fred right", fred.right()) print("Bill right", bill.right()) #fred.init(7,7) count = 12 while count > 0: #print(count) print("Fred looks at:", fred.look()) print("Fred forward",fred.forward()) print("Bill looks at:", bill.look()) print ("Bill forward",bill.forward()) count -= 1

print("Fred looks forward at", fred.look()[2]) # element 2 is forward view print("Bill looks forward at", bill.look()[2])

Note, if you load either the "Demo.map" or Test.map world into tthe simulator, the grobot.demo() will demonstrate the options and return values from the robot methods (functions). You can also import and use the grobot module (program) from the interactive shell and try out the commands interactively, e.g.:

        import grobot 
        grobot.demo() 
        fred = grobot.NewRobot("fred", 5, 5, "red") 
        fred.look() -> "wall" 
        fred.forward() -> "Bang" 
        fred.init() -> "OK"

