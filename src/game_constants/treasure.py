from enum import Enum

class Treasure(Enum):
    FIVE_HUNDRED_GOLD = "500 Gold"  # perception 1 reward
    BBQ_SAUCE = "BBQ_SAUCE"   # needed for mcnuggets 2nd quest
    SLOTS_VEST = "SLOTS-VEST"   #perception 2 chest
    INVITATION = "Invitation"
    RIB_DEMON_KEY = "rib demon key"



    @staticmethod
    def add_treasure_to_player(player, treasure):
        if treasure.value not in player.level_two_npc_state:
            player.level_two_npc_state.append(treasure.value)

    @staticmethod
    def add_quest_to_player(player, treasure):
        if treasure.value not in player.quest_items:
            player.quest_items.append(treasure.value)
