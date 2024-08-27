from enum import Enum

class Events(Enum):
    CHICKEN_QUEST_START = "CHICKEN_QUEST_START"
    QUEST_1_BADGE = "QUEST_1_BADGE"
    QUEST_1_COIN = "QUEST_1_COIN"
    QUEST_1_COMPLETE = "QUEST_1_COMPLETE"
    SLOTS_RIPPA_SNAPPA_DEFEATED = "SLOTS_RIPPA_SNAPPA_DEFEATED"
    BLACK_JACK_BLACK_MACK_DEFEATED = "BLACK_JACK_BLACK_MACK_DEFEATED"
    MC_NUGGET_FIRST_QUEST_COMPLETE = "MC_NUGGET_FIRST_QUEST_COMPLETE"  # win from rib demon slots
    MC_NUGGET_SECOND_QUEST_COMPLETE = "MC_NUGGET_SECOND_QUEST_COMPLETE" # bbq sauce is involved
    MC_NUGGET_THIRD_QUEST_COMPLETE = "MC_NUGGET_THIRD_QUEST_COMPLETE"
    MC_NUGGET_QUEST_1_REWARD = "MC_NUGGET_QUEST_1_REWARD"
    MC_NUGGET_QUEST_2_REWARD = "MC_NUGGET_QUEST_2_REWARD"
    MC_NUGGET_QUEST_3_REWARD = "MC_NUGGET_QUEST_3_REWARD"
    NUGGIE_SAUCE_1_FOUND = "NUGGIE_SAUCE_1_FOUND"
    NUGGIE_SAUCE_2_FOUND = "NUGGIE_SAUCE_2_FOUND"
    NUGGIE_SAUCE_3_FOUND = "NUGGIE_SAUCE_3_FOUND"
    SLOTS_VEST_FOUND = "SLOTS_VEST_FOUND"


    @staticmethod
    def add_event_to_player(player, event):
        if event.value not in player.level_two_npc_state:
            player.level_two_npc_state.append(event.value)

    def add_item_to_player(self, player, event):
        if event.value not in player.items:
            player.items.append(event.value)
