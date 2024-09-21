

import math

import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


# there should be 3 quest
# first 500 COINS
#  + 10 HP
#  THRID GOURMAND HAT


# quest marker npc items 2 we can store quest state there as well as talking state of quest whether we talked to npc already or 1st time
# need to add quest marker state

class MCNugg(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        self.npc_messages = {

            "level_6_quest": NpcTextBox(
                [
                    "MC Nugg: The rib demons have a special item, get it for me, either one is fine?",


                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_1_finish": NpcTextBox(
                [
                    "MC Nugg: very groovy hero here is your reward of perception glasses, very groove ",
                    "Hero: Thank you for this friend. ",
                    "You must have a shovel because you totally dig me"

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_2_start": NpcTextBox(
                [
                    "MC Nugg: listen up nugg brother, with a perception of 2 you can find my super bbq sauce item, you can either level up or equip the item i gave you",
                    "Hero: i'll check around "

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_2_finish": NpcTextBox(
                [
                    "MC Nugg: Good on you here is your reward of 500 coins .",

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_3_start": NpcTextBox(
                [
                    "MC Nugg: ok now its time for your final quest nugg brother, defeat the black jack dealer please",

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_3_finish": NpcTextBox(
                [
                    "MC Nugg: Good on you here is your reward for 3rd complete .",

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "final_message": NpcTextBox(
                [
                    "MC Nugg: final .",

                ],
                (50, 450, 50, 45), 30, 500
            ),

        }

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Reporter.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):

        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        min_distance = math.sqrt((player.collision.x - self.collision.x) ** 2 + (player.collision.y - self.collision.y) ** 2)

        if min_distance < 10:
            print("nooo")

        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt((player.collision.x - self.collision.x) ** 2 + (player.collision.y - self.collision.y) ** 2)

            if distance < 40 and state.player.menu_paused == False:
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                # Reset the message based on player state

                current_message = self.npc_messages["level_6_quest"]

                if Events.MC_NUGGET_FIRST_QUEST_COMPLETE.value in state.player.level_two_npc_state:
                    current_message = self.npc_messages["quest_1_finish"]
                if Events.MC_NUGGET_BETA_QUEST_COMPLETE.value in state.player.level_two_npc_state:
                    current_message = self.npc_messages["quest_2_start"]
                if Events.MC_NUGGET_SECOND_QUEST_COMPLETE.value in state.player.level_two_npc_state:
                    current_message = self.npc_messages["quest_2_finish"]
                if Events.MC_NUGGET_QUEST_2_REWARD.value in state.player.level_two_npc_state:
                    current_message = self.npc_messages["quest_3_start"]
                if Events.MC_NUGGET_THIRD_QUEST_COMPLETE.value in state.player.level_two_npc_state:
                    current_message = self.npc_messages["quest_3_finish"]
                if Events.MC_NUGGET_QUEST_3_REWARD.value in state.player.level_two_npc_state:
                    current_message = self.npc_messages["final_message"]

                current_message.reset()

    def update_talking(self, state: "GameState"):
        # this method casues it to skip to end of message this method is only temp



        current_message = self.npc_messages["level_6_quest"]

        if Events.MC_NUGGET_FIRST_QUEST_COMPLETE.value in state.player.level_two_npc_state:
            current_message = self.npc_messages["quest_1_finish"]
        if Events.MC_NUGGET_BETA_QUEST_COMPLETE.value in state.player.level_two_npc_state:
            current_message = self.npc_messages["quest_2_start"]
        if Events.MC_NUGGET_SECOND_QUEST_COMPLETE.value in state.player.level_two_npc_state:
            current_message = self.npc_messages["quest_2_finish"]
        if Events.MC_NUGGET_QUEST_2_REWARD.value in state.player.level_two_npc_state:
            current_message = self.npc_messages["quest_3_start"]
        if Events.MC_NUGGET_THIRD_QUEST_COMPLETE.value in state.player.level_two_npc_state:
            current_message = self.npc_messages["quest_3_finish"]
        if Events.MC_NUGGET_QUEST_3_REWARD.value in state.player.level_two_npc_state:
            current_message = self.npc_messages["final_message"]



        current_message.update(state)
        state.player.canMove = False

        if state.controller.isTPressed and current_message.is_finished():

            if (Events.MC_NUGGET_SECOND_QUEST_COMPLETE.value in state.player.level_two_npc_state and
                Events.MC_NUGGET_QUEST_2_REWARD.value not in state.player.level_two_npc_state):
                state.player.level_two_npc_state.append(Equipment.NUGG_QUEST_TWO_MONEY.value)
                state.player.money += 500
                state.player.level_two_npc_state.append(Events.MC_NUGGET_QUEST_2_REWARD.value)

            if (Events.MC_NUGGET_THIRD_QUEST_COMPLETE.value in state.player.level_two_npc_state

                    and Magic.SLOTS_HACK.value not in state.player.magicinventory):
                state.player.level_two_npc_state.append(Events.MC_NUGGET_QUEST_3_REWARD.value)

                state.player.magicinventory.append(Magic.SLOTS_HACK.value)


            if (Events.MC_NUGGET_QUEST_1_REWARD.value in state.player.level_two_npc_state and
                    Events.MC_NUGGET_FIRST_QUEST_COMPLETE not in state.player.level_two_npc_state):
                state.player.items.append(Equipment.SOCKS_OF_PERCEPTION.value)
                Events.add_event_to_player(state.player, Events.MC_NUGGET_BETA_QUEST_COMPLETE)

                state.player.level_two_npc_state.append(Events.MC_NUGGET_FIRST_QUEST_COMPLETE.value)


            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            state.player.canMove = True

    def draw(self, state):
        # Draw character sprite
        sprite_rect = pygame.Rect(5, 6, 18, 26)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw the correct message box based on the state of the NPC
        if self.state == "talking":

            current_message = self.npc_messages["level_6_quest"]

            if Events.MC_NUGGET_FIRST_QUEST_COMPLETE.value in state.player.level_two_npc_state:
                current_message = self.npc_messages["quest_1_finish"]
            if Events.MC_NUGGET_BETA_QUEST_COMPLETE.value in state.player.level_two_npc_state:
                print("Yippy")
                current_message = self.npc_messages["quest_2_start"]
            if Events.MC_NUGGET_SECOND_QUEST_COMPLETE.value in state.player.level_two_npc_state:
                current_message = self.npc_messages["quest_2_finish"]
            if Events.MC_NUGGET_QUEST_2_REWARD.value in state.player.level_two_npc_state:
                current_message = self.npc_messages["quest_3_start"]
            if Events.MC_NUGGET_THIRD_QUEST_COMPLETE.value in state.player.level_two_npc_state:
                current_message = self.npc_messages["quest_3_finish"]
            if Events.MC_NUGGET_QUEST_3_REWARD.value in state.player.level_two_npc_state:
                current_message = self.npc_messages["final_message"]

            current_message.draw(state)

