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






