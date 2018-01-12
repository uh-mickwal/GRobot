# Xpos, Ypos Display test

macro	define/2
	asect $2
$1:
mend

	define IOregRB, 	0xf0	# GRobot IO register in IO page
	define IOregHDG, 	0xf1	# Heading indicator LEDs (bit 0=N, 1=E, 2=S and 3=W
	define IOregXpos, 0xf2	# X position indicator
	define IOregYpos, 0xf3	# Y position indicator
	define IOregBtn,	0xf4	# Button pressed. Buton pressed bits 0 to 3, Bit 7, 1 if button new pressed.

	define 	look, 	0b10000000	# Just look, no move
	define	right,	0b10000001	# movement commands
	define	left, 	0b10000010
	define	forward,	0b10000100
	define	home,		0b10001000


	asect 0x00
	ldi 	r0, 0xef
	stsp	r0			# set stack below IO segment
#
# ########################################################################### MAIN PROGRAM

Main:	
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
	
	
	
halt

# Variables
Heading: 	dc 0b00000010 # = N, W= 0100, S = 1000, E=0001
Xpos:		dc 1		# Initial Xpos
Ypos:		dc 1		# Initial Ypos



end
