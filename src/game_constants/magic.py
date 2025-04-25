

from enum import Enum

class Magic(Enum):
    # coin flip
    DICE_FORCE = "Dice Force"
    HEADS_FORCE = "Force"  # All rolls are heads
    SHIELD = "Shield" # coin flip dedefends bad rolls
    # slots
    SLOTS_HACK = "HACK"  # pay 0 money for slots
    # craps
    CRAPS_LUCKY_7 = "Triple D"    #  roll a 3rd dice, thx lady luck
    GREED_METER = "pig meter" #  scoring a 95 or higher nets you +50% win on bets
    # opossum in a can
    SHAKE = "shake"
    PEEK = "peek" #level 3 using your wit you ask the dealer whats in the can
    #black jack
    BLACK_JACK_REDRAW = "redraw"   # sir leopold steals an ace so fast nobody sees it
    REVEAL = "reveal" # shows how many points enemy has
    # hi low
    FLUSH_DECK = "flush deck" # cuts deck in half
    # dice fighter
    BAD_LUCK = "bad luck" # affects enemy attack rolls
    GOOD_LUCK = "good luck" # adds + 3 to luck



    # On level 3 and 5 have a shop keeper
    # For pacing reasons we cannoot have more than 3 spells per level
    # For pacing reasons we cannot have more than 4 equipments per level









    @staticmethod
    def add_magic_to_player(player, magic):
        if magic.value not in player.magicinventory:
            player.magicinventory.append(magic.value)

# 1) slots-  hack - this spell is gotten by getting a level 2 in spirit - for 5 turns you only need to insert money 1 time
# 2)  craps - for the cone out roll increase chance of a 7 by 20% on a success of meter - mc nug gives this one.
# 3)  opposum in a can - avarice of greed - add + 50 coins per success but also lose - 100 coins on failure. - level 6
# 4)  coin flip  - force heads - forces heads for 1 coin flip - Alex gives this


# EXIT SPELL CAN BE SOEMTHING LATER ON LETS YOU GO BACK FROM A GAMBLING MATCH TO INN, A GLOBAL SPELL