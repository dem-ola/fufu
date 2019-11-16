This game was inspired by a coding challenge. I am slowly morphing it into a different-ish game. As such, I am not going to worry about version or release compatibilities until I get it to some stable state. 

You are about to play a board game of battling knights/players.

Simplified rules:
--------------------------------------------------------------
- thirteen (!) knights are spaced out on a 13 x 13 square board
- each knight has a randomly assigned starting attack and defence skill score
- there are nine weapons; eight free and one already held by one knight
- each weapon has its own randomly assigned score
- each knight can move around one step at a time
- the knight starting out with a weapon cannot move 
- a knight that moves offboard ('drowns') leaves its weapon behind
- any knight without a weapon finding a free weapon picks it up
- a knight acquiring a weapon gains the weapons attack and defence scores
- a knight can only have one weapon at a time
- a knight cannot switch weapons
- knights that end up on the same square will fight to the death
- a dead knight drops dead on the spot and drops its weapon
- winning knights, if without weapons, pick up those of dead knights, if any
- winning knights win a bonus
- there is no required winner: hypothetically the game can go on forever


Other important info further below but if you just want to get on and play:

Typical command line - flags in any combination
--------------------------------------------------------------
% python game.py            
- runs game and includes all stdout log
- there's a state of play output in a NumPy array
- you can still play if you don't have NumPy 

% python game.py -numpy     
- don't load numpy; also will not show board game
- in reality: game will skip numpy if not found anyway

% python game.py rand [n]
- runs randmoves.py first 
- [n] is an optional positive number of 
- game moves: if blank, default is used

% python
(to start environment eg IDLE)
>>> import game
>>> game.main()


constants.py
--------------------------------------------------------------
''' Non-changing variables '''
You shouldn't need to touch this except you're changing
the rules of the game

- starting coordinates for knights and items/weapons
- file name with the moves - default 'moves.txt'
- flags in moves.txt for start and end of moves list
- separator for moves (see below) - default is ':'


moves.txt
--------------------------------------------------------------
''' Game moves '''
Load any game moves file here. Note that the format is strict so
deviations are likely to cause errors and stop the game from starting

- first line: 'GAME-START' <- note CAPS
- each move on its own line eg R:S
- moves are all CAPS so r:s <- wrong
- must be 3 characters in length i.e. no gaps so 'R : S' <- wrong
- you can use a different separator eg R>S but you must add this to
  constants.py. Game uses regex so be careful, better not use a
  regex special character
- you can have newline gaps between moves - these will be skipped
  e.g.
  R:S
  R:E
  		<- gap here is ok - will be skipped
  B:N
  Y:W
  ... and so on
- last line: 'GAME END' <- note CAPS


game.py
--------------------------------------------------------------
''' Runs game '''
Just run the program!

- from command line: python game.py
- the script will:
  
  validate the input moves file - stops & error if invalid
      common errors include: /n at end of file, bad spelling,
      wrong case
  
  load a board game - this is a 13x13 NumPy array
      this is used to visualise game moves step by step
      will skip if it can't find Numpy
      you can skip NumPy board stdout prints with 
      	... command line flag -numpy
  
  load knights and weapons from constants.py
      
  step through each move in moves.txt observing rules of the game
  
  print activity to stdout ie screen or terminal
      - move step number nb game skips blank lines
      - moved: from (y, x) to (y, x)
      - comment on any weapons found, picked
      - comment if another knight already occupies square 
      - comment on any battle (winner, loser, scores)
      - game board visuals - this is a Numpy array
      - dictionary of knight positions: key=position, value=knight
      - dictionary of free weapons: key=position, value=weapon
  
  game board syntax:
      - first alpha charcter of knight or weapon eg R for Red
      - knights with no weapon eg R->0
      - knight with a weapon eg R->A == red holds axe
      - more than one knight on square eg R->A/Y->M
      - 'x' after knight is a dead knight eg Rx->0
      - drowned knights are not shown
      - free weapons on same square eg AM
      - free weapons on same square as knight eg H/G->D
  
  dump final position in a final_state.json file 


randmoves.py
--------------------------------------------------------------
''' optional: generates random game moves '''
Can be used for testing and playing around. Note that because
knights start at edge of game board it's easy for them to go
offboard and drown early in the game. To offset this tendency
the algorithm accepts an input to nudge nights inwards.

- set 'safe' percentage of moves for inward travel
- set number of moves
- writes output to whatever file is set in constants.py
  so overwrite this if you don't want to overwrite that file
- running:
  - from command-line (on it's own): python randmoves.py
  - from command line (as part of game): python game.py rand


final_state.json
--------------------------------------------------------------
''' Final psotions of knights and weapons '''
