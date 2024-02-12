# Casino Hell

A 2D Casino game written in Pygame.

Mini Games:
- Coin Flip
- Black Jack
- Craps
- Dice Fighter
- Nuke 'em
- Opossum in a Can

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

Every 3 levels gain a new spell
1, 4, 7,10, 13 ,16,19,

stat points:
10

to get players playing games daily have daily rewards. Rewards can be things such as heart points, food, money, exp etc etc

quest can also be " dont use magic" or anything else that will make the game harder.




How to start program:

 python src/main.py 
 

rib demon slots:
every time you lose you get plucked, but its hell so it regrows.
we cna have rib demons do 1/4 player HP damage or something like that
damage is done if all 3 spins land on a rib demon
having a high body  can deflect the rib snatchers  or even reduce damage

each game needs 2 stats attached to it







opossom guard: this item blocks opposum bites from doing damage
opossom repellant: 25% chance picking the wrong can wont result in a loss 

next up is the demons:
we need to have a few on the screen moving about
hedge hogs as well lets have 8 of them plus nurgle
hedge hogs go in the chilli to stir it around

demons be all like "the hedge hogs go in the chili to stir it aroudn where else would a hedge hog go?""
we are going in the hedge maze to gete something for the doctor  for the rabies cure.
"Come on out you little hoggers, time to get back in the chilli where you belong"
"If you come out now I promise not to put any ghost peppers in the chilli  next time.""
"Well thats nice of him"
"Last time I heard him say that he stayed true to his word, but they always add something even worse"

Rewards:
if one hedgeog found: save coin
If all 4 hogs are found: save coin + item

now going forward:
now the next step is game flow. 
Now before we make the game more tight, we need to make up our quests. 
here is the following step by step game flow:

For quest maybe have confirm boxes : "Do you have what I want Yes/No" Or maybe do a check afer dialgue box 
closes and if the item is there on close open up next dialog box

Main mission: get 2000 coins! You need 2000 coins to play against the bosses
2nd Mission:  beat opossum in a can to unlock next part whatever that is

mission 1: defeat cheating ted
There is going to be our first quest: beat him, and talk to cindy for your reward: Inn badge. Very easy battle!

Mission 2:
Talk to janet
she is the optional quest giver, at this point the other 5 npcs will show up. 
I feeel the best way to go forard is to delete the NPC, and replace it with another once defeated, this will
hard elimate any chances of going through menu by accident.

Her quests are as follows:
1) get a score of 400 on opossum in a can between either of hte two opossum in a can people(not boss). 
1) if both are defeated ,move on to next quest line.  
2) have a CHR of 1
3) find nurgle-hes in a trash can give a hint " he looooves to hang out in trash cans"


Mission 3:
Oh no you got rabies!
Oh shit you got the opossum demon rabies, go to the doctor, whom tells you there is a plant in the hedge maze

Mission 4:
talk to sir Leopold, hedgehog "knight" , who will tell you that his friends in the maze are also there. 
Now we go in hedge maze, rescue hedge hogs, get the plant, and collect our rewards!

Mission 5: By this point we are simply collecting enough coins to defeat the bosses and wrap up quests

Mission 6: defeat the boss and move on to nexxt area!


NPC text box has methods to start over from our len.index back to one which my Text boxes are missing
I'll need to go through the game bit by bit , improving everything to make it good.

For boss:
maybe have magic lock, but player increases luck + 1 
"Hahahaha now you are even less likely to win"
"Your wrong, now I'm more likely to win"
"that doesn't make any sense?"
"I didn't want to have to use this so soon in , but it looks likke i dont have much  of achoice, brings out lucky
coin and rubs it, +1 luck."
"His luck.....its radiating off of him like a blast furnace"

easy fix: 
Npcs are showing on text box, so just have npc posistions not intersect with a text box, 
easy fix lol

losing all your money turns you into a hedge hog or a horse

NOTE:
 change reveal to say low, medium or high score, 

i like this:

you need to give like 4000 coins which are held, if player wins the boss they get the coins back.
by giving coins player gains + 1 body, and this makes the game a little harder. 
But the +1 body and its rewards will be pretty tempting to our players.


for NPC

GAME BUG FIXES and NEEDED UPDATES:
Teleporters need fixing, selecting NO Still teleports
Need to update Bar to have a food item, roach burger, lots of protein 
Items need description when hoovering in shop
Need to fix it to where player can appear at fixed points on each map
need battle screen menus that explain rules and stamina drain and other info
need general info menu with player exp, leve ,items, 
no need to tell player how much gold and exp they gain , not like they going to read it, they can alwasy check menu
if player levels up in battle we could have a special screen pop up or perhaps eject player from battle?

I need to do the hotel room, and let the player equip items and magic spells

There is a bug: 
after winning coin flip you are stuck till you talk one last time.

i need to make an Screen and an NPC to practice messages and make "components"

have an intro screen "arent' you going to read it?"
Hero:"WHy it's like 30 pages, thats too much man"
demon: "Very well we hope you enjoy your stay *smiles*"

STORE SHOP HAS A BUG OF LEAVING AND AREA AND COMING BACK THE ITEMS ARE NO LONGER SOLD OUT

CINDY HAS BUGS WITH HER QUEST LINE TEXTS THEY KEEP PLAYING BACK TO THE START
NEED TO CHECK ITEM APPENDS AS WELL
THE OPPOSUMS HAVE A BUG THAT IF YOU GET THE SHOT THEN THE OTHER ONE WONT WANT TO TALK TO YOU

need to update coin flip screens so when magic is not there we simply have a blank space over magic , 
need to be conisstant 

oppossum in a can needs more messages to reflect all the state


BUG HUNT:

1) For all NPCS need to figure out:
2) Not letting player move during games
3) not letting player move during messages

####
####   BLACK JACK THOMAS NPC IS WORKING AS INTENDED IN REGARDS TO MOVING DRUING MESSAGES DURING TALKIGNA AND AFTER BATTLE
####
####


if we dont lick our hands and fingers clean they take it as an insult and they add more peppers and other
awful things, always leave with your hands and fingers clean.
If you try to leave with dirty hands you'll be licked clean like a cat, please don't make us do it.

Devils DUE README:
each player is giving 5 cards
6 community cards are laid out
each player takes turns having the buck
whover has buck gets to pick first
each round player has to either:
drop out
swap a card from community pile
make a bet and push money to devils pile
if you dont swap, you make a bet and stick with it till the end
at any phase you can drop out but you lose your monies
if your bet is in the devils pile you can only make 1 bet , but others can raise you 

maybe have sir leopold during his actions in combat  "I'll show you what real power looks like"


#####
#####
######

when using gimp be sure to set image to RGB values
https://graphicdesign.stackexchange.com/questions/39014/pngs-made-in-gimp-not-coming-out-transparent

How to remove background from GIMP
https://www.youtube.com/watch?v=PWZOMFFW9_0

demons:
https://www.spriters-resource.com/snes/demonscrest/

music:

bar-cutsscene 2
inspiring cinematic ambient
lexin_music

bar-cutscene 1
Kitchen | Blog | Positive | Travel | Happy
open music list

opossum in a can 
spy jazz
serge quadrado

coin flip
Time Hurries (Powerful Motivational Sci-Fi Cinematic War Music)
audiorezout

black jack
running free long edition
muzaproduction

maybe battle music
AUDIOREZOUT
Shooter Time (Aggressive Powerful Dark Motivational Sci-Fi Music)


boss music
Platinum (Powerful Sci-Fi Cinematic Futuristic Intense War Music)
AUDIOREZOUT

demon boss:
horror action
magnetic_trailer

inn sleep
are you sleeping jazzb
music for videos


chili area
life of a wandering wizard
sergeQuadrado

battle area/start  area/ boss area
The SPell-dark magic back ground music
OB-LIX

rest area
Night Jazz
Onoychenkomusic

hedge maze
let the mystery unfold
geoharvey

https://pixabay.com/music/search/

load start screen
Behind Dark Shadows - Dark Ambient Music For Horror And Mystery
ShadowsAndEchoes
https://pixabay.com/music/horror-scene-behind-dark-shadows-dark-ambient-music-for-horror-and-mystery-153820/


SOUND EFFECCTS:::

https://www.101soundboards.com/boards/10261-dragon-warrior-ii-sounds#goog_rewarded




######
#####
#####
######

in REST area there are two characters that are not having collisoin because we have them set to GLOBAL state.
we can solve this by putting a barrier and not draw it that way they cant walk through the NPC
86753


if I press the P key on any screen it opens up the plaeyr stats when yhou go back to start screen
but not the current screen

the doctor has a bug that her last message wont play twice you have to leave and enter screen

there is a bug that is giving me infinte spirit, hp and spirit

nelly is bugged she is not reducing player HP to 1

player must play 1 of each game in order to go to the boss.

We can force players to play opossum ina  can because thats where most of the money is.
THey wont even be able to beat the level without playing the game. 
the inn room needs to have a save book
player needs 2000 coins to get the body +1 potion

start gold 300
Earn 200 gold from coin flip
after finish start area
500 gold

gambling area
black jack - 300 gold
coin flip - 500 gold

opossum in a can - 1200 gold

-hold 2000 coins to get the TUFFness potion

Expected gold to spend:
400 for inn
500 for sir leopolds paw
200 for save coin
200 for bar items

chili area:
Oppossum in a can -1200
black jack -500 gold


Horse: we drink beer, then we make beer

have doctor opposum put up 100,000 coins for hero 


###
###
###
NOTE:
If player stamina is below 1: put them in doctors office, but charge 200 coins. 
if player stamina is below 10% perhaps have their HP Meter be red
if player coins are below 10: Game over....


if state.player.rabiesImmunity == True:
then we need something for each NPC for a new state to handle new messages, maybe a new message box?
not fully sure on how to handle it.


inn keeper needs fixing with his Yes message

lets put Janet in a new location if hero has rabies, and then move her back
when player no longer has it

black jack flow needs work, if you busts we dont see the final card,
also lets addd a score function that we can display for our ease of use.

put in game that Janet (quets giver) Is out fetchign the shop keeper and will be back later


####
####
BIG BUG:
state for our magic spells after being casts are still around, at least for opossum in a can .
#####

#####

Time to collect my thoughts:
Need the following:
Test game for bugs in regards to magic
Test game flow for hardness
Need everyone dialog change two more times
one time after we cure rabies
one time after we go to the inn twice
need to build out inn dialog
need to spend a good week buildign out the hedge maze which is going to probably be hard
need to fix collision as its STILL BROKEN
need to build out boss area
need to build demon boss
need to build out cut scenes
need to get this done by february and be ready to ship this out no later, thats 28  from now, 
which is probably 20-24 days of dev time.
need to fix black jack its still happening too fast
need graphics for opossum in a can 
need to build out save/load funciton to support quests completed
as well as money left of enmeies
need to build out game over for player if money drops below 0
need dto build out if player goes below 0 stamina

refactor 

refactor 

REFACTOR
#####


basing dialog boxes based on player state is what i should have done at the start, looking at quest janet for 
example I could have just made it to where BASED ON ITEMS IN PLAYER inven we could have based choices around that

you should not be able to leave any boss battles, once you in it ,its for the long haul

Demon:
I ccould tell you , that i'll rip your guts out and make you hang by em,
i could tell you that i'll make you eat giant piles of shit,l
I could even tell you that I'll bury you alive in crawling ants.
but you know what....I'll let you use your imagination,when we're done here i"m using
the orb of see thoughts, 

whatever feears you have deep down, whatever you think isthe worst that can happen,..
whatever horrifying things you can imagine...IS WHAT I'LL DO TO YOU!!!

you think we demons are jovial and nice, that we're a joke, well, i'll show you what true 
horror looks like, 

new item or companion: 2nd chance, if stamina goes below 1, your stamina is revived to 1/2
new items: 

stamina guard: if stamina falls below 0, restore up to 1 stamina
save coin : save for free at rest area if gold is 300+
teleport potion: teleport to rest area
stamina plus : + 5 stamina
magic plus : + 5 magic
money bag: 500coins



players need to have a perception of 1 to use shake

NOTE!!!
save coins should only work at rest area
unless we make the state checks that we have on rest screeen into a method and pass that method to every screen

after we get nurgle the hedge hog back lets have janet vanish and be replaced by a new NPC to better 
track state

have a check that when player buys soemthing at store its automatically sold out such as equip items
maybe have a state for each item, and wehn player buys item we set it to False, and then
if itemis set to False, its read as "sold out"

if we want to later on down the line we can have differnt save methods, and call them level 1 save etc etc
this way , when we save,we can start with brand new state. 

####
###
BUG FOUND IN BLACK JACK, IF THERE IS A MATCH, BETWEEN BOTH PLAYER AND ENEMY THEN DRAW DOES NOTHING AND ENDS THE ROUND
bug found, after we turn in blue flower we can't chat up with the doctor till we leave screen and come back.
sir leopold re appears even after he in my inventory

####

imagine random encounters with random game screens that pop up like a  Turn based JRGP.


######
######
######
MASTER FIXER LIST: GOING THROUGH GAME REAL TIME TO FIX ALL BUGS, GOING TO GET ALL THE WAY TO THE END ON THIS ONE.

* i might change how janet is handled, in regards to messages and quest so we dont have her in global
* still need to fix collision 
* still need to work on hedge maze

5) add sound effects when confirming something via button press such as with yes/no menus


20) need to build out demon boss encounter



27) need to make sure there are never empty dialog anywhere need to fine tooth comb and fix with blits

i think you can win double bet if you get black jack will need to investigate this

"i thought they were costumes"

"costumes!!! brother man your perception sucks, you need my help more than i thought. "

black jack demons crest, this means -20 gold each round for both parties

imrpove start load screen maybe have title flash wait 2 seconds then allow load/start

opossum in a can need to add money each time to the enemy money pool

need to fix salley 

am i getting money from opossum in a can nelly????
-ansewr to above yes, i need to fix how money works in that game

Here is my current TODO list:
fix NPCS messages, they are giving message based on either sir leopold or the blue flower when itshould
be based on rabies immunity.

I need to make sure that each game is a little unique
i like the final boss, that idea was a lot of fun. 
I need to update hedge hog sprites
I"ll have to think on demon sprites


I need to fix black jack messages so you cant select while talking, easy fix, 
need to fix magic menu
need to make sure all enemies have desperation state
 

need to set player postion more in middle need to figure that out but it wil be based on screen size



%%%%%%The below is the master bug list: %%%%%%%
sir leopold should be the exit condition
I need to fix things, when hero stamina hits 0 or lower, put him to the doctor office charge 100 coins for rescue
kick player out if their gold is below a threshold, game over if its 0 or lower. Need a game over screen state as
a global

opossum in a can goes through chompy messsages to fast for sally maybe nelly too need to check
there is a bug I htink the last can you picked isn't being reset in the list on refresh 
need sound effects for items that you cant buy like in ff6

need to set life to red when low on all screens 

fix TEXTBOX class similiar to NPC textz box for wrapping