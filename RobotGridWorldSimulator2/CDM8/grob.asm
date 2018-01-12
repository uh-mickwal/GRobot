macro	define/2
	asect $2
$1:
mend

	define  IOregRB, 0xf3		# robot IO register in IO page
	define  IOregKB, 0xf0		# keyboard IO register in IO page

	
	define	right,	0b10000001	# movement commands
	define	left, 	0b10000010
	define	forward,	0b10000100
	define	home,		0b10001000


	asect 	0x00
	ldi 	r0,0xef
	stsp	r0	# set stack below IO segment
#
############################################################################ MAIN PROGRAM

loop:
	ldi r3,IOregRB
	jsr getchar

	if
	   ldi r1,"h"
	   cmp r1,r0
	is eq
	   ldi r1,home
	   st  r3,r1
	fi

	if
	   ldi r1,"l"
	   cmp r1,r0
	is eq
	   ldi r1,left
	   st  r3,r1
	fi


	if
	   ldi r1,"r"
	   cmp r1,r0
	is eq
	   ldi r1,right
	   st  r3,r1
	fi

	if
	   ldi r1,"f"
	   cmp r1,r0
	is eq
	   if
	      ld r3, r1
	      ldi r0, 4
	      and r1,r0
	   is z			# the way forward is clear
	   	ldi r1,forward
	   	st  r3,r1
	   else
	      ldi r0,msg1
	      jsr println
	   fi
	fi
br loop


msg1:	dc	"Sir, can't move forward, Sir! we are blocked!",0x0d,0
############################ getchar() #####################################
############################################################################

getchar:		# get next character in r0, quict if 'q'
   save r1
   save r2
	ldi  r0, IOregKB

	do		# loop until keyboard ready
	  ld  r0,r1
	  tst r1
	until mi

	inc  r0		# r0->IOregKB_data
        ld   r0,r1	# ascii from keyboard to r1

	if
	   ldi r2,"q"
	   cmp r1,r2
	is eq
           halt
        fi

        inc  r0		# r0->screen data
        st   r0,r1	# r1 to screen -- echo

   move r1,r0		# return ASCII in r0

   restore
   restore
   rts

############################ printc() #####################################
###########################################################################
printc:			# print char in r0 on screen
save r1
		ldi r1,IOregKB+1	# monitor
		st r1,r0
restore
rts


############################ println() #####################################
############################################################################
println:		# print a NULL-terminated string pointed to by r0
save r1
	move r0,r1
	while
	   ldc r1,r0
	   tst r0
	stays nz
	   jsr printc
	wend
restore
rts










end
