from enum import Enum

class Events(Enum):
    ERIKA_IN_PARTY = "erika"
    CHICKEN_QUEST_START = "CHICKEN_QUEST_START"
    QUEST_1_BADGE = "Quest Badge" #coin flip 500 coins quest by alex
    QUEST_1_COIN = "Quest Coin"  #opossum in a can 500 coins quest by alex
    QUEST_1_COMPLETE = "QUEST_1_COMPLETE"

    SLOTS_RIPPA_SNAPPA_DEFEATED = "SLOTS_RIPPA_SNAPPA_DEFEATED" # this unlocks quest by Alice
    BLACK_JACK_BLACK_MACK_DEFEATED = "BLACK_JACK_BLACK_MACK_DEFEATED"
    OPOSSUM_IN_A_CAN_CANDY_DEFEATED = "OPOSSUM_IN_A_CAN_CANDY_DEFEATED"
    COIN_FLIP_BETTY_DEFEATED = "COIN_FLIP_BETTY_DEFEATED"
    CRAPS_HAPPY_DEFEATED = "CRAPS_HAPPY_DEFEATED"


    MC_NUGGET_FIRST_QUEST_COMPLETE = "MC_NUGGET_FIRST_QUEST_COMPLETE"  # win from rib demon slots
    MC_NUGGET_BETA_QUEST_COMPLETE = "MC_NUGGET_BETA_QUEST_COMPLETE"  # win from rib demon slots
    MC_NUGGET_SECOND_QUEST_COMPLETE = "MC_NUGGET_SECOND_QUEST_COMPLETE" # bbq sauce is involved
    MC_NUGGET_THIRD_QUEST_COMPLETE = "MC_NUGGET_THIRD_QUEST_COMPLETE"
    MC_NUGGET_QUEST_1_REWARD = "MC_NUGGET_QUEST_1_REWARD"
    MC_NUGGET_QUEST_2_REWARD = "MC_NUGGET_QUEST_2_REWARD"
    MC_NUGGET_QUEST_3_REWARD = "MC_NUGGET_QUEST_3_REWARD" # reward for beating black jack all coins
    NUGGIE_SAUCE_1_FOUND = "Erika 2nd invite"
    NUGGIE_SAUCE_2_FOUND = "NUGGIE_SAUCE_2_FOUND"
    NUGGIE_SAUCE_3_FOUND = "NUGGIE_SAUCE_3_FOUND"
    SLOTS_VEST_FOUND = "SLOTS_VEST_FOUND"
    STAT_POTION_AREA_2 = "STAT_POTION_AREA_2"
    SPIRIT_TWO_ALICE_QUEST = "Alice Invite"
    SPIRIT_TWO_ALICE_QUEST_FINISHED = "SPIRIT_TWO_ALICE_QUEST_FINISHED"

    # below is for level 3
    CRAPS_JUNPON_DEFEATED = "junpon defeated"
    BLACK_JACK_ALBERT_DEFEATED = "black jack albert defeated"


    @staticmethod
    def add_event_to_player(player, event):
        if event.value not in player.level_two_npc_state:
            player.level_two_npc_state.append(event.value)

    def add_item_to_player(player, event):
        if event.value not in player.quest_items:
            player.quest_items.append(event.value)
