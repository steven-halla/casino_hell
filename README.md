******# Casino Hell

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





How to start program:

 python src/main.py 
 

rib demon slots:
every time you lose you get plucked, but its hell so it regrows.
we cna have rib demons do 1/4 player HP damage or something like that
damage is done if all 3 spins land on a rib demon
having a high body  can deflect the rib snatchers  or even reduce damage

each game needs 2 stats attached to it



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





####
HUGE HUGE HUGE
REFACTOR TIME!!!!

1) Lets fix the issues that kenny said:
2) Give more hint for first guy
3) fix key inputs, should be asdf for commands not T, hell maybe I can go for controller support?
4) Fix messages some of them are not displaying correct
5) treasure chest primary class needs revamped, it should contain all the methods for displaying/opening and such
6) The demon class is checked, all methods are handled here except drawing/updating
7) I need to redo classes for text boxes. 
8) There should be a primary class for text boxes perhaps, no idea why I have it as an entity?
9)  How many text boxes do I need? 
10) the screen class needs a full refactor as all screens need to look the same.
11) I need to improve player status screen to have images
12) I need to have a level up system in place so when teh player levels up we give the player the info they need


play advancement for level 2:

the player levels:
at this point we can have + 3 levels


we can have a quest stat increase potion. 

We need 4 magic spells:
1 for slots  - hack: your coin last for 5 spins
1 for craps - increase come out roll probability 
1 for coin flip - forced heads - last for 1 turn forces the flip to be an automatic heads -make this one very expensive great for final push - make it a 50/50 chnace to work
1 for opposum in a can - drain - adds + 100 coins to pot if you get a X3 you get the coins last 5 turns

we need 4 items:
1 for black jack - if player bust gives 50% chance to disard the last card instead, players cannot redraw 
1 for hungry starving hippos - hippo takes an extra 3 seconds to appear on screen
1 for player boost -  + 20 hp + 10 mp
1 for craps - no stamina drain for point rolls 

1 stat potion - increase any stat from a 1 to a 2
1000 gold --
100 gold

2 save coins
+1 spirit gloves  adds spirit to you 

darlene's chicken nugget amulet - slots-adds + 20% chance that final roll will match first number good or bad
have  1 companion item slot
at level 5 perception allow a free slot for anything

For level 2:
body :2 - this lets the player eat chicken poodle soup  + 20 HP
mind 2: + 20 MP 
spirit 2: NPC gives player an item. also allows chicken nugget pendant to get equiped 
percption 2 : 2 chest
luck 2: global bonus 

level 4 is your level:

Level 5:
gain 10 HP / MP
gain new magic spell
Gain stat point

level 6:
gain 20 HP / MP

level 7:
gain 10 hp / mp
stat point

level 8:
stat point
gain 10 hp / mp
magic spell 

1 spell in treasure chest perception 2

1 spell for sale in shop

IMPORTANT
LETS INTRODCUCE LEVEL CHECKS FOR EXP GAINS, SO THAT IF A PLAYER IS AT A CERTIAN LEVEL THEY CANNOT GAIN EXP























