Final testing for all screens.

1) Game over for all screens works for loss of money and stamina
2) All spells work for enemies
3) All player spells have correct effect/duration baseed on stats
4) All Player items have correct/duraction based on stats
5) Can I leave the screen via quit and get to the right place
6) fix menu bug of not accessing menus close to enemy
7) Create bosses for area 3 and 4
8) update shops
9) make sure level up works for all screens
10) IF we are here then we only have a week left to finish project
11) Is all game screens set magic lock to false after an exit?
12) make sure that player cant leave while enemy spell active

LEVEL 1 CHECK List
Talked to an NPC Sally said NO and it put me in a strange spot no idea how i got in this bug
Sally opossum might have an issue with Money when creating a game for  first time maybe a good idea
to check each game to make sure they each have proper money ( do not save before doing this check)
Test level ups for all screens - COMPLETE








LEvel 2 check list
ANy screen with spells


        # --- Lock QUIT option if double-draw debuff is active ---
        if self.player_debuff_double_draw > 0:
            self.welcome_screen_choices[self.welcome_screen_quit_index] = "Locked Down"
        else:
            self.welcome_screen_choices[self.welcome_screen_quit_index] = "Quit"

this should lock it down for quit menu


CRAPS: 
check for instaneces of round rest and make sure everything triggers for this fun after bet totals 
also for craps test to maek sure betting works for both point and set screens
Make sure yuo can exit aftter first round, in the Game rest we reset the menu option

opossum in a can:
put the below in init methods 
self.welcome_screen_choices = ["Play", "Magic", "Quit"]self.welcome_screen_play_index = 0
self.welcome_screen_magic_index = 1
self.welcome_screen_quit_index = 2
the below is how we do lock down the above suupliements this
        if self.player_debuff_poison > 0:
            self.welcome_screen_choices[self.welcome_screen_quit_index] = "Locked Down"
        else:
            self.welcome_screen_choices[self.welcome_screen_quit_index] = "Quit"
