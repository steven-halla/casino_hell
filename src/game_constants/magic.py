

from enum import Enum

class Magic(Enum):
    HEADS_FORCE = "HEADS_FORCE"  # this is gained from alex quest
    SLOTS_HACK = "SLOTS_HACK"  # this is a level 2 tier reward from mc nugg
    CRAPS_LUCKY_7 = "CRAPS_LUCKY_7"    #  this is gained with mind 2
    REVEAL = "reveal"

    @staticmethod
    def add_magic_to_player(player, magic):
        if magic.value not in player.magicinventory:
            player.magicinventory.append(magic.value)

# 1) slots-  hack - this spell is gotten by getting a level 2 in spirit - for 5 turns you only need to insert money 1 time
# 2)  craps - for the cone out roll increase chance of a 7 by 20% on a success of meter - mc nug gives this one.
# 3)  opposum in a can - avarice of greed - add + 50 coins per success but also lose - 100 coins on failure. - level 6
# 4)  coin flip  - force heads - forces heads for 1 coin flip - Alex gives this


# EXIT SPELL CAN BE SOEMTHING LATER ON LETS YOU GO BACK FROM A GAMBLING MATCH TO INN, A GLOBAL SPELL