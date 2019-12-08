Rules
--------------------------------------------------------------
- each Fu has a randomly assigned starting attack and defence skill score
- there are nine weapons; eight free and one already held by the central Fu
- each weapon has a randomly assigned score
- Fus move one step in a ny direction
- the central Fu starting out with a weapon cannot move 
- a Fu that moves offboard ('drowns') leaves its weapon behind
- any Fu without a weapon finding a free weapon picks it up
- a Fu acquiring a weapon gains the weapons attack and defence scores
- a Fu can only have one weapon at a time
- a Fu cannot switch weapons
- Fus that end up on the same square fight to the death
- a dead Fu drops its weapon
- winning Fus, if without weapons, pick up those of dead Fus, if any
- winning Fus win a bonus
- there is no required winner: hypothetically the game can go on forever


Typical command line - flags in any combination
--------------------------------------------------------------
% python game.py            
- there's a state of play output in a NumPy array

% python game.py -numpy     
- don't load numpy; also will not show board game
- in reality: game will skip numpy if not found anyway

% python game.py rand [n]
- randomly generate [n] game moves to use


moves.txt
--------------------------------------------------------------
''' Game moves '''
Load any game moves file here. Note that the format is strict so
deviations are likely to cause errors and stop the game from starting

- first line: 'GAME-START' <- note CAPS
- each move on its own line eg R:S <- in caps; no gaps
- you can use a different separator eg R>S but you must add this to
  constants.py. Game uses regex so be careful, better not use a
  regex special character
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
  
  print activity to stdout ie screen or terminal
      - move step number nb game skips blank lines
      - moved: from (y, x) to (y, x)
      - comment on any weapons found, picked
      - comment if another Fu already occupies square 
      - comment on any battle (winner, loser, scores)
      - game board visuals - this is a Numpy array
      - dictionary of Fu positions: key=position, value=Fu
      - dictionary of free weapons: key=position, value=weapon
  
  game board syntax:
      - first alpha charcter of Fu or weapon eg R for Red
      - Fus with no weapon eg R->0
      - Fu with a weapon eg R->A == red holds axe
      - more than one Fu on square eg R->A/Y->M
      - 'x' after Fu is a dead Fu eg Rx->0
      - drowned Fus are not shown
      - free weapons on same square eg AM
      - free weapons on same square as Fu eg H/G->D
  
  dump final position in a final_state.json file 


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
- running:
  - from command-line (on it's own): python randmoves.py
  - from command line (as part of game): python game.py rand


final_state.json
--------------------------------------------------------------
''' Final psotions of Fus and weapons '''
