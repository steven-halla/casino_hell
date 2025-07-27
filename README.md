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
# I need to do more types in parameters of my funcs "such as state: 'gamestate'"
# !!!######################################################################



# if I decide to go forward with % chance for magic, this will mean an over haul
# stage 5 should focus on this 
# peek - maybe have 1 more  at level 3 and 5
# shake - at level 5 all oposum cans shake 

# STORY 1st screen
# after getting poinsoned by spell Hero: I get it now....you use magic, because your weak, you cant even gamble, can you? You think I'm going to feel
# feel or dispar because of you? Your pathetic and greedy, you have no love for the game
# You disgust me to no end, beating you is going to bring me great satisfaction 




TO DO LIST:
CREATE ALL BATTLE SCREENS FOR LEVELS 4 AND 5
CREATE ALL MAGIC SPELLS
CREATE ALL EQUIPMENT
REFACTOR EVERY FILE
FOR LEVEL 5 EVERYTHING NEEDS TO BE PERFECT AND TIGHT AS THAT WILL BE THE BASELINE FOR PREVIOUS SCREENS
CREATE MAPS
CREATE SOMETHING ELSE TO DO SUCH AS A MINI GAME OR SOMETHING
MAYBE PUZZLES?
REWORK SPIRETS
MUSIC
REEL SYSTEM FOR SLOTS- HOLD ACTION BUTTON , A BAR APPEARS, A THIN LINE GOES UP AND DOWN, 
EVERY ROUND WE CHANGE THE POINT , THIS WILL CHALLANGE THE PLAYER, PLAYER WILL PRESS DOWN BUTTON TO STOP METER
NEW SPELL OR EQUPIMENT - FREEZE THE SLOTS BAR
have the slot system work for up to 5 turns this way the player doesn't do that stuff all the time
this will set  a bonus or negative bonus depending-maybe need to test

#
# for level 4 to do:
# build poker, new game, update hungry hippos with runner, flesh out,single bets instead of 3
# hungry hippos include an audience 
# 



#



    # @typechecked
    # def update_player_lose_point_roll(self, state) -> str:
    #     if state.controller.confirm_button:
    #         self.round_reset(state)
    #         self.money += self.bet
    #         state.player.money -= self.bet
    #         self.game_state = self.WELCOME_SCREEN
    #         # this breaks
    #     return 1233

# i need to check the below in the future for type safety 
pip install mypy
mypy src/

board square types:
6 card squres (20%)
1 victory sqare ( pass go pay 1000 gold for token or go back to start) cash in exp if you pass
10 gold squres
6 exp squares
5 trap squares lose stamina
2 theif squres steals random gold


POKER SPELL: 
BLuff - Makes enemy fold depending on their hand
i could also make a bluff mechanic 

poker 


i can use the below:

use this for pop ups:
pygame.display.init

this may not work on mac os
pygame.display.set_mode((width, height), pygame.FULLSCREEN)

if so use this instead:
pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_mode((width, height))  # windowed mode

pygame.display.set_caption
Set the current window caption

pygame.display.get_num_displays
Return the number of displays

pygame.display.get_allow_screensaver
Return whether the screensaver is allowed to run.
pygame.display.set_allow_screensaver
Set whether the screensaver may run


heat



: New idea;
WIth a high perception instead of uncovering t chest how about we lower shop prices
 The below code has menus working

      if state.player.current_screen == "" and state.controller.start_button:
            state.player.current_screen = "main_menu_screen"
            state.player.canMove = False

        # If in any menu-related screen, just draw the player menu logic
        if state.player.current_screen.endswith("_screen"):
            state.player.draw_player_stats(state)


we are in the mid stretch

BAR UPDATAE:
for body  1 allow player to raise a stat of thier choice perhaps?
also allow an exp option
for player have update using EVENTS of boss defeated for exp caps

QUest: 
maybe you cant defeat an enemy without first completing quesst. 
could be that if you "beat the enemy" They are giving fake monies? '
I could also do "pracrice for quest?"


I need to have enemies for building EXP/getting quest that dont expire

stats level 1:

defeat coinflip ted - gets 1 ,mind point
eat at the bar - get 1 body point
earn level 3 - get 1 spirit point
get 2000 coins - get 1 perception point
fight boss- get 1 luck point

STATS:
BODY - HP BONUS - DAMAGE REDUCTION -EXTRA FOOD
MIND - MORE MP - MORE SPELLS - SPELL IMPROVEMENTS
SPIRIT - HIGHER CHANCE FOR EQUIPMENT TO LAND EFFECTS - REDUCTION IN STORE COST - MORE POWER EQUIPMENT MODIFIERS 
PERCEPTION - HOLD MORE ITEMS - EQUIP MORE ITEMS
LUCK - BONUS TO ALL GAMES 

level 2:
1 craps item - store

1 craps spell - level 2 mind
1 opossum in a can spell - store

1 coin flip item - store
1 slot magic - prize
1 hippo item - prize
hp bracelet - store





















we build an array ["",""", ""]
variable turn counter = 8
for loop

for i in variable turn counter:
    
       level 1-- self.shop_items = [Equipment.BLACK_JACK_HAT.value, Equipment.OPOSSUM_REPELLENT.value,Equipment.MP_BRACELET.value, Magic.REVEAL.value,  Events.LEVEL_1_BOSS_KEY.value ]
        level 2--     self.shop_items = [
            Equipment.COIN_SAVE_AREA_2.value,
            Equipment.COIN_FLIP_GLASSES.value,
            Equipment.HEALTHY_GLOVES.value,
            Magic.SHAKE.value,
            Equipment.BOSS_KEY.value,# i need to change this to EVENT
            Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value
        ]





equipment
Level 1 - black jack, opossum in a can, Neatrual
level 2 - coin fip, craps, neatural, hungry starving hipppos, 
level 3 -  dice fighter, slots, neatural, opossum in a can,nuetral, 
level 4 -   hungry starving hippos, coin flip, black jack, hi/low, poker, wheel of torture, nuetral

magic
level 1 - reveal-black jack , shield - black jack,  - 2
level 2 - shake - opossum in a can, lucky 7-craps, hack-slots, - 3
level 3 -  flush deck-high/low, badluck-dice fighter, force heads-coin flip, redraw- black jack - 4
level 4 -  wheel of torture, poker, craps,  slots  - 4

------------------------

Level 1
self.shop_items = [
BLACK_JACK_HAT - black jack -protects from bust
OPOSSUM_REPELLENT -opossum in a can - reduce damage from bites
MP_BRACELET - increase in MP
magic - REVEAL  -Black Jack - shows enemy hand points 
]
magic 1 - shield - Coin Flip -  defneds from bad choices

Level 2
self.shop_items = [
        COIN_FLIP_GLASSES -coin flp - adds more money on wins
        HEALTHY_GLOVES - incrase in HP
        Magic - SHAKE -opposum in a can - Shake opossum cans
        Equipment - DARLENES_CHICKEN_NUGGER_AMULET -Craps- extra luck on missed power roll, and other benifits
    ]
hippo prize equipment- hippos hour glass - hangry angry hippos - extra time for hippo to arrive
slots prize magic- - hack - slots - dont pay money to play slots game
magic 2 - lucky  7 - craps - more able to rolls better 

Level 3
self.shop_items = [ 
    LUCKY_ROTTEN_SOCKS - Dice fighter - DOES NOT DO ANYTHING!!!!!!!!!!!!!!!!!!!!!!!!!!!
    SPIRIT_SHOES - adds + 1 to spirit
    magic - heads force - coin flip - forces heads every time
    magic - BLACK_JACK_REDRAW -black jack - make enemy redraw
    magic - FLUSH_DECK - hi low - 13 card deck
]
hippo prize equipment- backwards watch - hangy angry hippos - slows down non picks
slots prize equipmnt - slots shoes - slots - more money on jck pot and more hp and mp
magic 3 bad luck - dice fighter - worse rolls on defense

Level 4
self.shop_items =[
CoinFlipGloves -Coin flip - alllows + 200 on bets for coin flip
HighLowPants - hilow - adds extra spread factor
POker bracelet  - poker - player will no longer draw any 2 cards
WHeel Dice - wheel of torture -  DOES NOT DO ANYTHING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
LUCKY Human's Foot - general - adds +1 LUCK
magic - poker - Swap - DOES NOT DO ANYTHING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
magic - Greed -craps - DOES NOT DO ANYTHING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
]

Hippo prize equipment - SirLeopoldsAmulet - black jack - protects with aces and other benifits
Slots prize Magic - LUCKY777 - slots - DOES NOT DO ANYTHING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Could have it to where if you get a 777 on first slot then all of them get that
magic 4 - Dice force -wheel of torture- THIS SPELL DOES NOT DO ANYTHING
