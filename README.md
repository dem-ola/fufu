This game was inspired by a coding challenge. I am slowly morphing it into a different-ish game. As such, I am not going to worry about version or release compatibilities until I get it to some stable state. 

This is a game of 13 warriors, each a Fu (as in ShiFu) but with only 9 weapons arranged on 13 x 13 board. One centrally placed Fu has a weapon at start. Fus move one square at a time, rather like pawns in chess, and meeting Fus fight.

See DOCUMENTATION for rules.

To play
--------------------------------------------------------------
% python game.py            
- there's a state of play output in a NumPy array

% python game.py -numpy     
- don't load numpy; also will not show board game
- in reality: game will skip numpy if not found anyway

% python game.py rand [n]
- randomly generate [n] game moves to use