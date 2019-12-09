This game was inspired by a coding challenge. I am slowly morphing it into a different-ish game. As such, I am not going to worry about version or release compatibilities until it's in some stable state. 

Overview
--------------------------------------------------------------
FuFu ia a game of 13 martial warriors, each a Fu (as in ShiFu) but with only nine weapons arranged on 13 x 13 board. Each Fu has randomly assigned attack and defence skill scores. Only one Fu has a starting weapon. Fus move one square at a time, rather like pawns in chess, and meeting Fus fight.

% python game.py
--------------------------------------------------------------
''' Runs game '''

Rules
--------------------------------------------------------------
- only the centrally placed Fu starts out with a wepon
- the central Fu starting out with a weapon cannot move 
- weapons have randomly assigned scores
- Fus move one step in any direction
- a Fu that moves offboard ('drowns') leaves its weapon behind
- any Fu without a weapon finding a free weapon picks it up
- a Fu acquiring a weapon gains the weapons attack and defence scores
- a Fu can only have one weapon at a time and cannot switch
- Fus that end up on the same square fight to the death
- a dead Fu drops its weapon
- winning Fus, if without weapons, pick up those of dead Fus, if any
- winning Fus win a bonus
- there is no required winner: hypothetically the game can go on forever

moves.txt
--------------------------------------------------------------
''' Game moves '''
Load any game moves file here. Or run randmoves.py to generate random moves.

- first line: 'GAME-START' <- note CAPS
- each move on its own line eg R:S <- in caps; no gaps
- you can use a different separator eg R>S but you must add this to
  constants.py. Game uses regex so be careful, better not use a
  regex special character
- last line: 'GAME END' <- note CAPS

randmoves.py
--------------------------------------------------------------
''' optional: generates random game moves '''
Can be used for testing and playing around. Note that because
Fus start at edge of game board it's easy for them to go
offboard and drown early in the game. To offset this tendency
the algorithm accepts an input to nudge nights inwards.

- set 'safe' percentage of moves for inward travel
- set number of moves
- writes output to whatever file is set in constants.py
  so overwrite this if you don't want to overwrite that file
- from command-line (on it's own): python randmoves.py