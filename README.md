******# Casino Hell

below are for sprits for money
https://gif-superretroworld.itch.io/interior-pack

https://opengameart.org/content/tilesets-and-backgrounds-pixelart

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
sound effects for when bite

Black jack:
sound effects for laying down cards
Need to fix text boxes in my init method to be more uniform
maybe show sir leopold on screen when he steals on ace or have him dart across screen 

slots:
sound effects while putting in coin, pulling lever,wheel spinning



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
slots 999- gain an extra 50 HP 50 MP and 100 gold on jack pot
hippo silver ticket - win extra coins the more people survive that you pick - global
agile hands: blow command: win every init roll

Magic:
spell: Loaded Dice: for attack rolls, a 1 cannot be rolled, last 1 turn - mind level 3
spell: redraw - asks enemy to redraw one of thier face up cards - quest 
spell: Order: Re inislitze the trash cans, keeping your score.





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

comands:
attack- rolls 3d6
defend - rolls 1d6 when you have a match
bet-when you break increase bet

`
priest: removes curses for a feee
new idea for stat boosters: curse the item cannot be removed,not only do you have to go and rest, but also have to
pay a fee for curse removal
should set max to 4, as in if you have 4 perception the item wont do you any good. 5 is special. 
player room - this is  where player goes after staying at inn
all items not equipped after rest go in treasure chest
controller support

player does triple roll
enemy does triple roll



level 3:

new game: Spin the cards
match starts with a small card battle, such as high/low, or who has highest card, or some other thing
but I want the player to be able to use a little strategy.

BLACK JACK:
swap  = enemy can swap a card of thiers for one of yours
lock draw  - unable to use draw command

COIN FLIP:



draw_card

x position
blit the card


split phase:
self.player hand
self.enemy hand
split
split modifier
new_range = []

player_split_low self.player_score - self.split
player_split_high self.player_score + self.split

new_range.append(player.splitlow , player.splithigh)
if self.player_score in rage of new_range
    print("player wins)
else:
    print("Player loses)]]




Level 3 to do list:
create shop keeper
create bar keeper
create magic keeper - can only buy  1 magic

update hungry starving hippos graphics


there are 18 total magic spells
THere are 25 total equipment pieces 

# i still need luck for coin flip




# quest can involve talking to all NPC or beating witin X number of turns
# inventory allow player ot have 1 item in inventory per perception point 1, 2, 3


# all missed content can get bought, for a heavy price

# each level should have a magic that can be bought in a shop
# level 3 no magic  quest but have 3 spells in shop and 1 you can learn 
# allow magic to empower magic % chance
# allow spirit to empower items 
# maybe have some items to help with mazes and stuff
# magic and equipment should nto be missable by proxy of failing quest
on the bottom not sure what is best approach between what leve you get things
# spirit of 4 should empwer compaion items
# spirit of 5 should empower compaion items to affect more games and better bonues for base games


# I need to make a fun that displays an image
# first lets display teh full image
# then lets do a section 
# then do 3 sections and store each one as a param
# cycle through the images\

# level one i am ok having 6 screens with 500 gold each to make it easier on player
# i nee to work on quest
# i need to creaet something in game to take up time and create a relief from gambling / talking
# lets have hidden journals this could maybe be a good idea



# a food that lets you save DO NOT DELETE THese LINeS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!############
# boss on level 4 can be fought anytime (we weant to give the player a sense of how powerful
# they are , for players wanting a challange they'll know they can procedd forward just fine.)
# THE BELOW ARE MY THOUGHTS ON EQUIPMENT AND MAGIC
# SPIRIT CAN MAKE ITEMS STRONGER AT LEVEL 3 , LEVEL 4 WE GET NEW COMPANION ITEM LAW DEMON,LEVEL 5 IMPROVE COMPANION ITEMS PLUS MORE QUEST
# PERCEPTION WE CAN HAVE AN INVENTORY LEVEL 2 AND 4 WE GET EXTRA SPACE 3 AND 5 WE CAN EQUIP MORE ITEMS, PLUS MORE CHEST
# MAGIC WE CAN HAVE STRONGER SPELLS LEVELS 3 5 WE GET STRONGER MAGIC % ON SOME GAMES AND 2 4 WE GET LONGER DURATIONS, MORE MP
# HEALTH WE CAN HAVE MORE HP, AND FOOD , AT LEVELS 3 5 WE GET DAMAGE REDUCTIO
# LUCK BETTER % CHANCE FOR ALL GAMES 
# FOR BALANCE WE SHOULD PROABLY THINK MORE ON THIS
# maybe create items to incrase spell chance, spell duratin, and equipment effectiveness
# This could in fact be bonuses giving to companion items for a 5 spirit-
# !!!######################################################################



# if I decide to go forward with % chance for magic, this will mean an over haul
# stage 5 should focus on this 
# peek - maybe have 1 more  at level 3 and 5
# shake - at level 5 all oposum cans shake 








