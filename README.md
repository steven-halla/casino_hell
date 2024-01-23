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



-current considerations: 
lets build all NPCs in one room
this will include inn keeper, shop keeper,lets
keep it stupid simple

lets also flesh out the stats
all start at level 1, max level 6

-luck  - 
-trickster- cheat mode activated 
-intellect  - 
-body  - affects hit/magic points as well as how much food you can eat
-charisma - higher scores helps with NPC Interactions can also open unique character dialouge  

perks Field:Alwyas active
perks battle : always active
spells: gain advantages in battle
NPcS: sometimes having a perk of a certain level gets you stuff in interactions

Luck:
Field : sometimes you can find items , higher luck gives better items from chests sometimes 
NPC: Certain interactiosn having high luck can make an interaction go one way or another. be sure
to have audio/visual ques
Battle: depends on the game. Black jack will have enemy get worse cards depending on your luck.
Spell: black  jack: reshuffle hand 3 times. 
SPell: Ace, increse chance of getting an ace by 25%

Perception:
Feild: certain chest are now visible to you, or perhaps we can have an highlight for invis items
battle: alerts player when NPC is cheating, this is used to help you bet low
spell: 

Games:
1) coin flip
2) black jack
3) oppsum in a can 
4) hungry starving hippos
5) poker
6) dice fighter
7) nuke em
8) slots


trade face down card. 

perks: 
At every 4 levels gain a perk. 

perks: Every level give player a choice out of 3
HP ^
MP ^
FP ^
Stat Boost: add +1 to a stat of 1
Level 1 perks:
Black Jack:  +10% to get an ace on your initial hand
Coin Flip: adds + 10
Oppusum in a can: +5% to your winnings


to get players playing games daily have daily rewards. Rewards can be things such as heart points, food, money, exp etc etc

quest can also be " dont use magic" or anything else that will make the game harder.

quest giver janet has 3 quests:
one is a simple fetch item quest to give her  a bottle of water
the second quests is to rescuse hodge podge the hedge hog from the maze (1 of 10 hedge hogs that are hidden)
the third quest is to defeat one of the bosses,like fully defeat this will unlcok her final convo . 

Rewards:
first is a spell for black jack
2nd is a save coin
3rd is an item that gives a bonus for black jack to help with final boss of the level

lets not forget to add the doctor for fixing opposum status



How to start program:

 python src/main.py 
 
lets add random messsages that play on the bet screen no reason to see the same text
over and over again 
maybe do this via a counter say every 10 games we can change the welcome messge
this means all games will need to back to the welcome screen
or we just make a new screen type that only triggers on counter of 10

rib demon slots:
every time you lose you get plucked, but its hell so it regrows. 
having a high body  can deflect the rib snatchers  or even reduce damage

each game needs 2 stats attached to it



opossum in a can game states:
Welcome screen-has welcome message
THere is no need for a bet screen

pick_screen
if you are here, subtract money from player pool

play again screen: select play again or quit 

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