
from enum import Enum

class Equipment(Enum):
    BLACK_JACK_HAT = "Black Hat"  # reward from Alice
    REFRESH = "refresh" # black jacks gain +20 stamina
    HIPPO_SHOES = "HIPPO_SHOES"  # testing only
    HIPPO_HOUR_GLASS = "HIPPO HOUR GLASS"  # level 3 perception
    SOCKS_OF_PERCEPTION = "Cool Shades"  # complete level 3 mc nugg quest
    NUGG_QUEST_TWO_MONEY = "NUGG_QUEST_TWO_MONEY"  # quest reward for mcnug
    BOSS_KEY = "boss key"
    OPOSSUM_REPELLENT = "opossum repellent"



    COIN_SAVE_AREA_2 = "COIN_SAVE_AREA_2" # BUY IN SHOP ONE TIME USE
    RE_EQUIP_AREA_2 = "RE_EQUIP_AREA_2" # BUY IN SHOP ONE TIME USE
    HEALTHY_GLOVES = "HEALTHY GLOVES"   # can be bought in shop
    STAT_POTION_AREA_2 = "STAT_POTION_AREA_2" # ONE TIME USE BUY IN SHOP - MAKE 2 K SO PLAYER HAS TO DEFEAT 1 SCREEN TO EARN

    SIR_LEOPOLD_AMULET = "sir leopold amulet"
    DARLENES_CHICKEN_NUGGER_AMULET = "Nuggie Amulet" # complete main quest chicken nugger sauce

    CRAPS_WRIST_WATCH = "craps wrist watch" # blow command

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