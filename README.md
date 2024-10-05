******# Casino Hell

A 2D Casino game written in Pygame.

Mini Games:
- Coin Flip
- Black Jack
- Craps
- Dice Fighter
- Nuke 'em
- Opossum in a Can

## How to perform unit test, last part is name of file

## python -m unittest tests.equipment_to_player_test


## Setup

System Installs Python 3, Pip, and Venv
```bash
brew install python
```

Configure Venv
```bash
python3 -m venv venv
source venv/bin/activate
```

Install project dependencies
```bash
pip install -r requirements.txt 
```

Run game
```bash
python src/main.py
```

## Tools 

- Tiled Map Editor
- Pygame


Games:
1) coin flip
2) black jack
3) oppsum in a can 
4) hungry starving hippos
5) poker -devils due
6) dice fighter
7) nuke em
8) slots


How to start program:

 python src/main.py 
 

when using gimp be sure to set image to RGB values
https://graphicdesign.stackexchange.com/questions/39014/pngs-made-in-gimp-not-coming-out-transparent

How to remove background from GIMP
https://www.youtube.com/watch?v=PWZOMFFW9_0

---------------------------------------
Game is now complete for 2nd round

Improvements going forward:
Coin Flip: 
Need a spinning coin
Need a "coin board" for graphics
Need to rethink how phases work, it works but I feel I could do better
sound effect for when coin is flipped and lands


Opposum in a can:
Need to show what the player picked on the screen so its not empty
sound effects for when bite

Black jack:
need to slow down dealing of cards for both player and AI
put a limit of 5 cards for draw.
sound effects for laying down cards
Need to fix text boxes in my init method to be more uniform

slots:
sound effects while putting in coin, pulling lever,wheel spinning
more graphcis that looks like a slot machine

Craps:
limit of 7 rolls during point phase 8th roll should always finish the round 
maybe give player bonus luck points option by betting extra gold?
dice sound effects

Hungry starving hippos:
mix up runners randomly
use tokens instead of letter number combos
add light graphics for swim area
space swimmers a tiny bit
program a better way for announcer to talk plays

Text /NPc Boxes
need to do testing and create/improve methods for use cases:
when message is at -1 index and finished nad player pushes T

No more absoulte paths need to work around that

























--------------