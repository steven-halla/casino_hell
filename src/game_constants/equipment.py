
from enum import Enum


class Equipment(Enum):

    # stats need to be more sacred its going to make shit too hard going forward
    # increasign luck + 1 is the only exception

    #level 1
    COIN_FLIP_GLASSES = "coin flip glasses" # spirit 3 adds + 20 spirit 5 add + 50 to cins
    OPOSSUM_REPELLENT = "opossum repellent" # more spirit = more dam reduction

    #level 2
    HIPPO_HOUR_GLASS = "HIPPO HOUR GLASS"  # level 3 perception  at level 3 spirit add + 1 second
    SOCKS_OF_PERCEPTION = "Cool Shades"  # complete level 3 mc nugg quest
    BLACK_JACK_HAT = "Black Hat"  # reward from Alice
    HEALTHY_GLOVES = "HEALTHY GLOVES"   # can be bought in shop + 10 hp per spirit

    #companion items
    SIR_LEOPOLD_AMULET = "sir leopold amulet" #companion item
    DARLENES_CHICKEN_NUGGER_AMULET = "Nuggie Amulet" # complete main quest chicken nugger sauce
    LAW_BOOK = "law book" # companion item level 3 at vert start of level 4


        # the below are for level 3 or EXPERIMENT
    CRAPS_WRIST_WATCH = "dice wrist watch" # blow command for all dice games
    COIN_FLIP_GLOVES = "coin flip gloves" # increase bet amount by +200 for CoinFlip
    SLOTS_SHOES = "slots shoes" # gives player + 100 hp and 50 focus on jackpot
    MP_BRACELET = "mp bracelet" # gives player 30 MP
    HIGH_LOW_PANTS = "high low pants" # This item gives +1 spread via spirit higher spreads take more HP
    # but this adds depth as player cna still get enemy ace great way to burn cards

    # level 3 and 4 below
    LUCKY_CHARM = "lucky charm" # + 1 to luck
    CHEFS_HAT = "chefs hat" # + 30 HP AND + 1 FOOD PER DAY
    MEDIUM_VEST = "medium vest"  # -20 opposum and slot demon damage
    HIGH_VEST = "medium vest"  # -30 opposum and slot demon damage and game 10
    SPIRIT_CHARM = "spirit charm" # + 1 spirit lvl 4



    # from quest and other
    NUGG_QUEST_TWO_MONEY = "NUGG_QUEST_TWO_MONEY"  # quest reward for mcnug
    BOSS_KEY = "boss key"
    COIN_SAVE_AREA_2 = "COIN_SAVE_AREA_2" # BUY IN SHOP ONE TIME USE
    RE_EQUIP_AREA_2 = "RE_EQUIP_AREA_2" # BUY IN SHOP ONE TIME USE
    STAT_POTION_AREA_2 = "STAT_POTION_AREA_2" # ONE TIME USE BUY IN SHOP - MAKE 2 K SO PLAYER HAS TO DEFEAT 1 SCREEN TO EARN

    # for testing
    HIPPO_SHOES = "HIPPO_SHOES"  # testing only




    @staticmethod
    def add_equipment_to_player(player, equipment):
        if equipment.value not in player.items:
            player.items.append(equipment.value)
            player.level_two_npc_state.append(equipment.value)

    @staticmethod
    def add_potion_to_player(player, equipment):
        if equipment.value not in player.items:
            player.level_two_npc_state.append(equipment.value)

    @staticmethod
    def add_item_to_quest_state(player, equipment):
        if equipment.value not in player.quest_items:
            player.quest_items.append(equipment.value)






# 1) BLACK JACK - BLACK HAT- IF YOU BUST GETS RID OF LAST CARD, AND YOU HAVE TO STAND -QUEST FROM ALICE
# 2) HIPPO_SHOES - HIPPO TAKES 3 SECONDS EXTRA TO APPEAR -SELL AT SHOP
# 3) gourmand hat - gain an extra food slot food cant be higher than 2 -MC NUGG REWARD LEVEL 3
# 4) SLOTS-VEST - GODO OR BAD + 10% CHANCE FOR 3RD ROLL TO MATCH FIRST ROLL -RIB DEMON SLOTS PRIZE
# 6) BODY VEST= +20 HP + 10 MP  - WE CAN BUY THIS AT THE SHOP - CHEST
# 8) darlenes nugget amulet - 1/2 stamina drain for point rolls - COMPLETE QUEST FOR DARLINE THE CHICKEN