# GRobot Demo Program V1
# M L Walters, April, 2016

macro	define/2
	asect $2
$1:
mend

	define IOregRB, 	0xf0	# GRobot IO register in IO page
	define IOregHDG, 	0xf1	# Heading indicator LEDs (bit 0=N, 1=E, 2=S and 3=W
	define IOregXpos, 0xf2	# X position indicator
	define IOregYpos, 0xf3	# Y position indicator
	define IOregBtn,	0xf4	# Button pressed. Button pressed bits 0 to 3, Bit 7, 1 if button new pressed.
	define IOregDbg,	0xf5	# Debug port

	define 	look, 	0b00000000	# Just look, no move
	define	right,	0b00000001	# movement commands
	define	left, 	0b00000010
	define	forward,	0b00000100
	define	home,		0b00001000
	
	# Variables in data memeory
	define	Heading, 	0x00
	define	Xpos, 	0x01
	define	Ypos,		0x02
	define	Sensors,	0x03

macro rand/1 # Return (not very!) random number between 0 to 255 in rn
	ldi $1, Xpos
	ld $1, $1 # Load Xpos
	ldc $1, $1 # Load code value pointed to by Xpos
mend


Start:
	asect 0x00
	

	asect 0x00
	ldi 	r0, 0xf0
	stsp	r0			# set stack below IO segment
#
# ########################################################################### MAIN PROGRAM

Main:
	# Wait for button to be pressed
	ldi r0, IOregBtn
	do
		ld r0, r1
		tst r1 	
	until mi # Bit 7; 1=0 button pressed
	#ldi r0, IOregXpos # Debug
	#st r0, r1		# Debug
	if 
		ldi r2, -124 # Home button = 4 
		cmp r1, r2
	is eq
		jsr ActHome
	fi
	if
	ldi r2, -121 #Forward button = 7
	cmp r1, r2
	is eq
		jsr ActFwd
	fi
	if 
	ldi r2, -122 # Right button = 6
	cmp r1, r2
	is eq
		jsr ActRight
	fi
	if 
	ldi r2, -123 # Left button = 5
	cmp r1, r2
	is eq
		jsr ActLeft
	fi
	if
	ldi r2, -125 # RUN Button
	cmp r1, r2
	is eq
		jsr Userprog
	fi
	
br Main # Loop forever!
halt # Just in case!


# ################### User Program (activated by RUN button
Userprog:	# Robot wanders around, avoiding walls, with random moves.
	# Check if Run/Stop button pressed
	ldi r1, look
	jsr Action # get sensor values. Note if error will (pop) rts back to Main
Loopst:
	if
		ldi r2, IOregBtn
		ldi r3, -125 # Home button = 4 and bit 7
		ld r2, r0
		cmp r0, r3
	is eq
		rts
	fi
	# Select move 
	# get possible moves
	
	# r1 now contains Sensor values
	# Then a bit of "randomisation"
	#rand r2
	#or r2, r1		# randomize r1
	ldi r3, IOregDbg
	st r3, r1		# Debug r1
	if 
		ldi r2, 0b00010000 # Turn left if clear  
		and r1, r2
	is z
		jsr ActLeft

	fi
	if 
		ldi r2, 0b00000100 # Go forward if clear 
		and r1, r2
	is z
		jsr ActFwd
	else
		jsr ActRight # Otherwise, turn right
	fi
br Loopst # Do again
	
# ################### Subroutines		
ActHome:	# Initialise to Heading = N, Xpos=1, Ypos=1
	# Returns sensor bits in r1, or 0b01100000
	ldi r1, home
	jsr Action # r1 = For init home, only comm/fatal error possible 
	ldi r3, Heading
	ldi r2, 0b00000010 # heading = N
	st r3, r2 
	ldi r3, IOregHDG # Update display
	st r3, r2
	ldi r3, Xpos 	# Xpos
	ldi r2, 1 
	st r3, r2	# Xpos = 1
	ldi r3, IOregXpos
	st r3, r2
	ldi r3, Ypos # Ypos = 1
	st r3, r2
	ldi r3, IOregYpos 
	st r3, r2
rts
		
		
ActFwd:	 # Forward
	ldi r1, forward
	jsr Action # returns error sensor data in r1
	# Note r1 not changed by this subr
	# Update Xpos and Ypos and dusplays
	ldi r2, Heading
	ld r2, r2 	# get current heading
	ldi r3, Ypos 
	ld r3, r3	# Load Ypos
	if # Heading = N
	ldi r0, 0b00000010 # N 
	cmp r2, r0
	is eq 
		inc r3
	fi
	if # Heading = S
	ldi r0, 0b00001000 # S 
	cmp r2, r0
	is eq 
		dec r3
	fi
	# Store Ypos, even if it has not changed!
	ldi r0, Ypos # Update Ypos
	st r0, r3
	ldi r0, IOregYpos # Update display
	st r0, r3
	# Then Xpos
	ldi r3, Xpos 
	ld r3, r3	# Load Xpos
	if # Heading = E
	ldi r0, 0b00000001 # E
	cmp r2, r0
	is eq 
		inc r3
	fi
	if
	ldi r0, 0b00000100 # W 
	cmp r2, r0
	is eq 
		dec r3
	fi
	# Again, store, even if not changed
	ldi r0, Xpos # Get Xpos
	st r0, r3
	ldi r0, IOregXpos # Update display
	st r0, r3
rts
		
		 
ActLeft:
	ldi r1, left
	jsr Action		
	ldi r3, Heading
	ld r3, r3 	# get previous heading
	shl r3
	if 
	ldi r2, 0b00010000
	and r3, r2
	is nz
		ldi r3, 0b00000001
	fi
	br StHdg # Skip to store heading
ActRight:
	ldi r1, right
	jsr Action
	ldi r3, Heading
	ld r3, r3
	shr r3
	if # Check for overflow
	tst r3
	is z
		ldi r3, 0b00001000
	fi 
StHdg: # Store heading, even if not changed
	ldi r2, Heading
	st r2, r3
	ldi r2, IOregHDG # Update LEDs 
	st r2, r3
rts	

Action: # Robot action passed in r1. 
	# Returns r1 = (Bits 6 = Fatal error, bit 5 = Collision) or (bits 0 to 4 sensor readings (1 = blocked)).
	# Do action
	ldi r0, IOregRB  # Robot IO port
	st  r0, r1		# Do the action
	# Check for collision (or error)
	ldi r2, 0b10000000
	# Wait until returned data is valid
	do
		ld r0, r1
		and r1, r2
	until nz
	# Test for errors
	if 
	ldi r2, 0b01100000 
	and r1, r2 # keep r1
	is nz # If error skip update displays and x, y and heading variables
		pop r2 # Skip updating displays  (dirty programming! Saves >10 bytes!)
		#ldi r0, IOregDbg 
		#st r0, r1		# Debug r1
	else
		# Store current Sensor data 
		ldi r2, 0b00011111
		and r2, r1 # Just leave bits 0 to 5 
		ldi r0, Sensors
		st r0, r1
	fi
	
	
rts	


#asect 0xf4
#	dc 0b10000010 # button 4 = Home Button for emulator testing
end 
