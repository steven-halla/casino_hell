from enum import Enum

class Treasure(Enum):
    FIVE_HUNDRED_GOLD = "500 Gold"
    BBQ_SAUCE = "BBQ_SAUCE"


    @staticmethod
    def add_treasure_to_player(player, treasure):
        if treasure.value not in player.level_two_npc_state:
            player.level_two_npc_state.append(treasure.value)