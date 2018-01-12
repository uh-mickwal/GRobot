
CdM-8 Assembler v2.1 <<<grobotDemo.asm>>> 08/04/2016 19:31:07

                  1  # GRobot Demo Program V1
                  2  # M L Walters, April, 2016
                  3  
                  4  macro   define/2
                  5          asect $2
                  6  $1:
                  7  mend
                  8  
                  9          define IOregRB,         0xf0    # GRobot IO register in IO page
                 10          define IOregHDG,        0xf1    # Heading indicator LEDs (bit 0=N, 1=E, 2=S and 3=W
                 11          define IOregXpos, 0xf2  # X position indicator
                 12          define IOregYpos, 0xf3  # Y position indicator
                 13          define IOregBtn,        0xf4    # Button pressed. Button pressed bits 0 to 3, Bit 7, 1 if button new pressed.
                 14          define IOregDbg,        0xf5    # Debug port
                 15  
                 16          define  look,   0b00000000      # Just look, no move
                 17          define  right,  0b00000001      # movement commands
                 18          define  left,   0b00000010
                 19          define  forward,        0b00000100
                 20          define  home,           0b00001000
                 21  
                 22          # Variables in data memeory
                 23          define  Heading,        0x00
                 24          define  Xpos,   0x01
                 25          define  Ypos,           0x02
                 26          define  Sensors,        0x03
                 27  
                 28  
                 29  Start:
                 30          asect 0x00
                 31  
                 32  
                 33          asect 0x00
00: d0 f0        34          ldi     r0, 0xf0
02: c8           35          stsp    r0                      # set stack below IO segment
                 36  #
                 37  # ########################################################################### MAIN PROGRAM
                 38  
                 39  Main:
                 40          # Wait for button to be pressed
03: d0 f4        41          ldi r0, IOregBtn
                 42          do
05: b1           43                  ld r0, r1
06: 05           44                  tst r1
07: e5 05        45          until mi # Bit 7; 1=0 button pressed
                 46          #ldi r0, IOregXpos # Debug
                 47          #st r0, r1              # Debug
                 48          if
09: d2 84        49                  ldi r2, -124 # Home button = 4
0b: 76           50                  cmp r1, r2
0c: e1 10        51          is eq
0e: d6 30        52                  jsr ActHome
                 53          fi
                 54          if
10: d2 87        55          ldi r2, -121 #Forward button = 7
12: 76           56          cmp r1, r2
13: e1 17        57          is eq
15: d6 4b        58                  jsr ActFwd
                 59          fi
                 60          if
17: d2 86        61          ldi r2, -122 # Right button = 6
19: 76           62          cmp r1, r2
1a: e1 1e        63          is eq
1c: d6 8e        64                  jsr ActRight
                 65          fi
                 66          if
1e: d2 85        67          ldi r2, -123 # Left button = 5
20: 76           68          cmp r1, r2
21: e1 25        69          is eq
23: d6 7d        70                  jsr ActLeft
                 71          fi
                 72          if
25: d2 86        73          ldi r2, -122 # RUN Button
27: 76           74          cmp r1, r2
28: e1 2c        75          is eq
2a: d6 2f        76                  jsr Userprog
                 77          fi
                 78  
2c: ee 03        79  br Main # Loop forever!
                 80  
2e: d4           81  halt # Just in case!
                 82  
                 83  
                 84  # ################### User Program (activated by RUN button
                 85  Userprog:
                 86  
                 87  
2f: d7           88  rts
                 89  
                 90  # ################### Subroutines
                 91  ActHome:        # Initialise to Heading = N, Xpos=1, Ypos=1
                 92          # Returns sensor bits in r1, or 0b01100000
30: d1 08        93          ldi r1, home
32: d6 a2        94          jsr Action # r1 = For init home, only comm/fatal error possible
34: d3 00        95          ldi r3, Heading
36: d2 02        96          ldi r2, 0b00000010 # heading = N
38: ae           97          st r3, r2
39: d3 f1        98          ldi r3, IOregHDG # Update display
3b: ae           99          st r3, r2
3c: d3 01       100          ldi r3, Xpos    # Xpos
3e: d2 01       101          ldi r2, 1
40: ae          102          st r3, r2       # Xpos = 1
41: d3 f2       103          ldi r3, IOregXpos
43: ae          104          st r3, r2
44: d3 02       105          ldi r3, Ypos # Ypos = 1
46: ae          106          st r3, r2
47: d3 f3       107          ldi r3, IOregYpos
49: ae          108          st r3, r2
4a: d7          109  rts
                110  
                111  
                112  ActFwd:  # Forward
4b: d1 04       113          ldi r1, forward
4d: d6 a2       114          jsr Action # returns error sensor data in r1
                115          # Note r1 not changed by this subr
                116          # Update Xpos and Ypos and dusplays
4f: d2 00       117          ldi r2, Heading
51: ba          118          ld r2, r2       # get current heading
52: d3 02       119          ldi r3, Ypos
54: bf          120          ld r3, r3       # Load Ypos
                121          if # Heading = N
55: d0 02       122          ldi r0, 0b00000010 # N
57: 78          123          cmp r2, r0
58: e1 5b       124          is eq
5a: 8f          125                  inc r3
                126          fi
                127          if # Heading = S
5b: d0 08       128          ldi r0, 0b00001000 # S
5d: 78          129          cmp r2, r0
5e: e1 61       130          is eq
60: 8b          131                  dec r3
                132          fi
                133          # Store Ypos, even if it has not changed!
61: d0 02       134          ldi r0, Ypos # Update Ypos
63: a3          135          st r0, r3
64: d0 f3       136          ldi r0, IOregYpos # Update display
66: a3          137          st r0, r3
                138          # Then Xpos
67: d3 01       139          ldi r3, Xpos
69: bf          140          ld r3, r3       # Load Xpos
                141          if # Heading = E
6a: d0 01       142          ldi r0, 0b00000001 # E
6c: 78          143          cmp r2, r0
6d: e1 70       144          is eq
6f: 8f          145                  inc r3
                146          fi
                147          if
70: d0 04       148          ldi r0, 0b00000100 # W
72: 78          149          cmp r2, r0
73: e1 76       150          is eq
75: 8b          151                  dec r3
                152          fi
                153          # Again, store, even if not changed
76: d0 01       154          ldi r0, Xpos # Get Xpos
78: a3          155          st r0, r3
79: d0 f2       156          ldi r0, IOregXpos # Update display
7b: a3          157          st r0, r3
7c: d7          158  rts
                159  
                160  
                161  ActLeft:
7d: d1 02       162          ldi r1, left
7f: d6 a2       163          jsr Action
81: d3 00       164          ldi r3, Heading
83: bf          165          ld r3, r3       # get previous heading
84: 2f          166          shl r3
                167          if
85: d2 10       168          ldi r2, 0b00010000
87: 4e          169          and r3, r2
88: e0 8c       170          is nz
8a: d3 01       171                  ldi r3, 0b00000001
                172          fi
8c: ee 9b       173          br StHdg # Skip to store heading
                174  ActRight:
8e: d1 01       175          ldi r1, right
90: d6 a2       176          jsr Action
92: d3 00       177          ldi r3, Heading
94: bf          178          ld r3, r3
95: 93          179          shr r3
                180          if # Check for overflow
96: 0f          181          tst r3
97: e1 9b       182          is z
99: d3 08       183                  ldi r3, 0b00001000
                184          fi
                185  StHdg: # Store heading, even if not changed
9b: d2 00       186          ldi r2, Heading
9d: ab          187          st r2, r3
9e: d2 f1       188          ldi r2, IOregHDG # Update LEDs
a0: ab          189          st r2, r3
a1: d7          190  rts
                191  
                192  Action: # Robot action passed in r1.
                193          # Returns r1 = (Bits 6 = Fatal error, bit 5 = Collision) or (bits 0 to 4 sensor readings (1 = blocked)).
                194          # Do action
a2: d0 f0       195          ldi r0, IOregRB  # Robot IO port
a4: a1          196          st  r0, r1              # Do the action
                197          # Check for collision (or error)
a5: d2 80       198          ldi r2, 0b10000000
                199          # Wait until returned data is valid
                200          do
a7: b1          201                  ld r0, r1
a8: 46          202                  and r1, r2
a9: e0 a7       203          until nz
                204          # Test for errors
                205          if
ab: d2 60       206          ldi r2, 0b01100000
ad: 46          207          and r1, r2 # keep r1
ae: e0 b3       208          is nz # If error skip update displays and x, y and heading variables
b0: c6          209                  pop r2 # Skip updating displays  (dirty programming! Saves >10 bytes!)
                210                  #ldi r0, IOregDbg
                211                  #st r0, r1              # Debug r1
b1: ee b9       212          else
                213                  # Store current Sensor data
b3: d2 1f       214                  ldi r2, 0b00011111
b5: 49          215                  and r2, r1 # Just leave bits 0 to 5
b6: d0 03       216                  ldi r0, Sensors
b8: a1          217                  st r0, r1
                218          fi
                219  
                220  
b9: d7          221  rts
                222  
                223  
                224  #asect 0xf4
                225  #       dc 0b10000010 # button 4 = Home Button for emulator testing
                226  end

======================================================================

SECTIONS:
Name	Size	Relocation offsets


ENTRIES:
Section		Name/Offset

$abs		<NONE>

EXTERNALS:
Name		Used in


======================================================================
