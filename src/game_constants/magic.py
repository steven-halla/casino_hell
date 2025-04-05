

from enum import Enum

class Magic(Enum):
    HEADS_FORCE = "Force"  # this is gained from alex quest but will have to redo
    SHIELD = "Shield" # coin flip dedefends bad rolls

    SLOTS_HACK = "HACK"  # this is a level 2 tier reward from mc nugg

    CRAPS_LUCKY_7 = "Triple D"    #  this is gained with mind 2
    REVEAL = "reveal"
    SHAKE = "shake"

    #the below are experiments OR level 3
    BLACK_JACK_REDRAW = "redraw"   # we get this level 3 quest
    PEEK = "peek" #level 3 using your wit you ask the dealer whats in the can
    FLUSH_DECK = "flush deck"
    BAD_LUCK = "bad luck" # dice fighter

    GREED_METER = "pig meter" #  scoring a 95 or higher nets you +50% win on bets


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