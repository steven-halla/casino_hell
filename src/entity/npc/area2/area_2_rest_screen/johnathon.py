

import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class Johnathon(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        # the below is how i will implement this in the future


        # DEFAULT_MESSAGE = "default_message"
        #
        # self.npc_messages = {
        #     DEFAULT_MESSAGE: NpcTextBox(
        #         [
        #             "Johnathon:If you want in the nugg den you need to prove yourself, reach level 6 and I'll let you inside to have all the juicy crispy chicken nuggies your little heart desires",
        #             "Opossum in ao teach you.....it will be less so.",
        #         ],
        #         (50, 450, 50, 45), 30, 500
        #     )
        # }

        # Integrated textbox content into guy_messages
        self.npc_messages = {
            "default_message": NpcTextBox(
                [
                    "Johnathon:The nugg koop only allows player level 6 or higher.",
                    "Johnathon: Once you're in, You can eat all the delcious crispy chicken nuggz your heart destires",
                    "Hero: Whats the catch?",
                    "Johnathon: oh no catch, you just might not like where they come from",

                ],
                (50, 450, 50, 45), 30, 500
            )
        }

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Shipping Workers.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):
        if self.state == "waiting":
            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":
            # Determine which message to use based on player state
            current_message = self.npc_messages["default_message"]


            if current_message.message_index == 1:
                if state.controller.isAPressed and pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"


                elif state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"

            self.update_talking(state, current_message)

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
                current_message = self.npc_messages["default_message"]

                current_message.reset()

    def update_talking(self, state: "GameState", current_message):
        current_message.update(state)
        state.player.canMove = False

        if state.controller.isTPressed and current_message.is_finished():
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            state.player.canMove = True

    def draw(self, state):
        # Draw character sprite
        sprite_rect = pygame.Rect(103, 6, 17, 23)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw the correct message box based on the state of the NPC
        if self.state == "talking":
            current_message = self.npc_messages["default_message"]
            current_message.draw(state)

