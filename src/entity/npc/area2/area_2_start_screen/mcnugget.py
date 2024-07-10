

import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

# there should be 3 quest
# first
#
#


class MCNugg(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        self.npc_messages = {
            "no_level_6": NpcTextBox(
                [
                    "MC Nugg: Yo Cuzz, sorry but you need to level up to level 6. My other quests needs a perception of 2, do you dig me?. ",


                ],
                (50, 450, 50, 45), 30, 500
            ),
            "level_6_quest": NpcTextBox(
                [
                    "MC Nugg: Now that your strong enough go beat mack-jack, that guy stole something form me. You can find him somewhere. Beat him and I'll reward you, do you dig me?",


                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_2_complete": NpcTextBox(
                [
                    "Alice: As i made a promise here is your back jack item",
                    "Hero: Thank you for this friend. "

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_2_complete_after_message": NpcTextBox(
                [
                    "Alice: I can give you a hint.",

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

            if distance < 40:
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                # Reset the message based on player state
                if state.player.level < 6:
                    current_message = self.npc_messages["no_level_6"]
                else:
                    current_message = self.npc_messages["level_6_quest"]





                current_message.reset()

    def update_talking(self, state: "GameState"):

        if state.player.level < 6:
            current_message = self.npc_messages["no_level_6"]
        else:
            current_message = self.npc_messages["level_6_quest"]

        current_message.update(state)
        state.player.canMove = False

        if state.controller.isTPressed and current_message.is_finished():


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
            if state.player.level < 6:
                current_message = self.npc_messages["no_level_6"]
            else:
                current_message = self.npc_messages["level_6_quest"]

            current_message.draw(state)

