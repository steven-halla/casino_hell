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
- Gimp


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
maybe show sir leopold on screen when he steals on ace or have him dart across screen 

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

Need to create bank
Need to create room for Player to equip items after resting.

Need to re format battle and map screens to be more uniform

Improve input validation and error handling.
I need to do validations for my code its a bit messy in that regard


Huanted house:
have a room with multiple chest but it takes 3 seconds per chest, have a timer after opening chest
this means the faster you clear area the more chest you can open before monster gets to you.

The haunted house should have 3 floors
upper floor
main floor
and the dreaded basement.
start out with 30 or so NPCS
and get less and less
lets hve it to where you can help other NPCS or hinder

3rd floor:
magic spells
redraw: black jack force enemy to redraw face up card


equipment:
craps blow- this opens the blow commnad
mind hat - + 30 mp
body belt: adds + 1 to body
opossum guilty shoes- if score is above 800 and you lose , retain 200 points
slots 999- gain an extra 25 HP 25 MP and 100 gold on jack pot
hippo ticket - win extra coins the more people survive that you pick - global
loaded dice - + When you are attacker and get a double that is less than defender, adds +1 to all 3 dice.
spell: Loaded Dice: 
triples - instant win
doubles - re roll 1 dice

battle dice:
Attacker role- you are trying to break the point
Defender role: you have set up the break point by rolling doubles, your job is to roll triples, no need to re roll doubles, just the 3rd dice.
if triples on first roll and win condition, player wins triple pot.
Triple 6 at any point wins double pot
both players roll 3d6, highest value goes first, if tie re roll
both players roll 3d6 ( 1 at a time), if two dice say 2 twos, re roll 3rd dice on next turn
other player can break this by getting doules of a higher value. 
if you get a higher double roll, you break the opponent ponit roll and they have to roll 3d6 to break your roll or match to win
first to match 3 numbers wins (higher or equal to break point)
each time abreak happens, the breaker has the chance to increase the pot, and other player can settle or go in.
in order to win, you need tripples of same value or higher than opponet. 

`


priest: removes curses for a feee
new idea for stat boosters: curse the item cannot be removed,not only do you have to go and rest, but also have to
pay a fee for curse removal
should set max to 4, as in if you have 4 perception the item wont do you any good. 5 is special. 
player room - this is  where player goes after staying at inn
all items not equipped after rest go in treasure chest
controller support
maybe allow 1 extra item slot for player for having high spirit?

dice fighter- 3 v 3 match
warrior: 10 hp  3 DD 0 spell cards 2 def dice
priest:  12 HP  2 DD 2 spell cards 3 def dice
wizard:  8 HP   1 DD 4 spell cards 1 def dice
roll to see which hero you target
dice fighter you cannot quit this match its all or nothing

























