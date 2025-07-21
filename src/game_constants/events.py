from enum import Enum

class Events(Enum):
    OPOSSUM_POISON = "OPOSSUM_POISON"
    REFRESH = "REFRESH"
    ERIKA_IN_PARTY = "erika"
    CHICKEN_QUEST_START = "CHICKEN_QUEST_START"
    QUEST_1_BADGE = "Quest Badge" #coin flip 500 coins quest by alex
    QUEST_1_COIN = "Quest Coin"  #opossum in a can 500 coins quest by alex
    QUEST_1_COMPLETE = "QUEST_1_COMPLETE"

    #level 2 below






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
    STAT_POTION_AREA_3 = "STAT_POTION_AREA_3"
    SPIRIT_TWO_ALICE_QUEST = "Alice Invite"
    SPIRIT_TWO_ALICE_QUEST_FINISHED = "SPIRIT_TWO_ALICE_QUEST_FINISHED"




    #below is for level 1------------------------------------------------------------------

    COIN_FLIP_TED_DEFEATED = "COIN_FLIP_TED_DEFEATED"
    COIN_FLIP_FRED_DEFEATED = "COIN_FLIP_FRED_DEFEATED"
    OPOSSUM_IN_A_CAN_SALLY_DEFEATED = "OPOSSUM_IN_A_CAN_SALLY_DEFEATED"
    BLACK_JACK_THOMAS_DEFEATED = "BLACK_JACK_THOMAS_DEFEATED"
    LEVEL_1_BOSS_DEFEATED = "LEVEL_1_BOSS_DEFEATED"
    LEVEL_1_INN_KEY = "LEVEL_1_INN_KEY"
    LEVEL_1_BOSS_KEY = "LEVEL_1_BOSS_KEY"

    #below is for level 2---------------------------------------------------------------
    BLACK_JACK_MACK_DEFEATED = "BLACK_JACK_MACK_DEFEATED"
    SLOTS_RIPPA_SNAPPA_DEFEATED = "SLOTS_RIPPA_SNAPPA_DEFEATED"  # this unlocks quest by Alice
    OPOSSUM_IN_A_CAN_CANDY_DEFEATED = "OPOSSUM_IN_A_CAN_CANDY_DEFEATED"
    COIN_FLIP_BETTY_DEFEATED = "COIN_FLIP_BETTY_DEFEATED"
    CRAPS_HAPPY_DEFEATED = "CRAPS_HAPPY_DEFEATED"
    LEVEL_2_BOSS_DEFEATED = "LEVEL_2_BOSS_DEFEATED"

    FEAST_CONSUMED = "FEAST_CONSUMED"
    LEVEL_SAVE_COIN_AREA_TWO  = "LEvel 2 save coin"

    # below is for level 3--------------------------------
    CRAPS_JUNPON_DEFEATED = "junpon defeated"
    BLACK_JACK_ALBERT_DEFEATED = "black jack albert defeated"
    COIN_FLIP_DEXTER_DEFEATED = "coin flip dexter defeated"
    OPOSSUM_IN_A_CAN_BILLY_BOB_DEFEATED = "opossum in a can billy bob defeated"
    DICE_FIGHTER_SIR_SIEGFRIED_DEFEATED = "dice fighter sir siegfried defeated"
    SLOTS_BROGAN_DEFEATED = "slots brogan defeated"
    HUNGRY_STARVING_HIPPOS_HIPPY_DEFEATED = "hungry starving hippos hippy defeated"
    HIGH_LOW_DIENA_DEFEATED = "high low diena defeated"
    HANGRY_ANGRY_HIPPOS_BEFF = "hangry angry hippos beff"
    BOSS_BLARPEON_DEFEATED = "boss blarpeon defeated"

    SLOTS_LEVEL_3_SECRET_ITEM_ACQUIRED = "slots_level_3_secret_item_acquired"

    # below is level 4:
    COIN_FLIP_BONNIE_DEFEATED = "coin flip bonnie defeated"
    BLACK_JACK_JASMINE_DEFEATED = "BLACK_JACK_JASMINE_DEFEATED"
    CRAPS_NABA_DEFEATED = "naba defeated"
    DICE_FIGHTER_SOPHIA_DEFEATED = "dice fighter sophia defeated"
    HIGH_LOW_CODY_DEFEATED = "high low cody defeated"
    HUNGRY_STARVING_HIPPOS_DIPPY_DEFEATED = "hungry starving hippos dippy defeated"
    OPOSSUM_IN_A_CAN_SILLY_WILLY_DEFEATED = "opossum in a can silly willy defeated"
    SLOTS_JURAGAN_DEFEATED = "slots juragan defeated"
    WHEEL_OF_TORTURE_VANESSA_BLACK_DEFEATED = "WHEEL OF torture vanessa black defeated"

    HANGRY_ANGRY_HIPPOS_DIPPY_DEFEATED = "hangry angry hippos DIPPY DEfeated"
    SLOTS_LEVEL_4_SECRET_ITEM_ACQUIRED = "slots_level_4_secret_item_acquired"




    # below is level 5:
    COIN_FLIP_WANTON_DEFEATED = "coin flip wantan defeated"
    BLACK_JACK_FENGUS_DEFEATED = "BLACK_JACK_FENGUS_DEFEATED"
    CRAPS_WIMPLETON_DEFEATED = "Craps_Wimpleton_DEFEATED"
    HUNGRY_STARVING_HIPPOS_NIPPY_DEFEATED = "hungry starving hippos nippy defeated"
    OPOSSUM_IN_A_CAN_BUBBA_DEFEATED = "OPOSSUM_IN_A_CAN_BUBBA_DEFEATED"
    SLOTS_BURBADAN_DEFEATED = "SLOTS_BURBADAN_DEFEATED"










    @staticmethod
    def add_event_to_player(player, event):
        if event.value not in player.level_two_npc_state:
            player.level_two_npc_state.append(event.value)

    @staticmethod
    def add_level_one_event_to_player(player, event):
        if event.value not in player.level_one_npc_state:
            player.level_one_npc_state.append(event.value)

    @staticmethod
    def add_level_two_event_to_player(player, event):
        if event.value not in player.level_two_npc_state:
            player.level_two_npc_state.append(event.value)

    @staticmethod
    def add_level_three_event_to_player(player, event):
        if event.value not in player.level_three_npc_state:
            player.level_three_npc_state.append(event.value)

    @staticmethod
    def add_level_four_event_to_player(player, event):
        if event.value not in player.level_four_npc_state:
            player.level_four_npc_state.append(event.value)

    @staticmethod
    def add_level_five_event_to_player(player, event):
        if event.value not in player.level_five_npc_state:
            player.level_five_npc_state.append(event.value)

    def add_item_to_player(player, event):
        if event.value not in player.quest_items:
            player.quest_items.append(event.value)
