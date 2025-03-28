

import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.events import Events


class Lunky(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        self.npc_messages = {
            "default_message": NpcTextBox(
                [
                    "Lunky: All of the gamblers gathered here, though you dont have to defeat all 5. Take things at your own pace.",
                    "Lunky: If a game is too hard try coming back later when you acheive higher levels, better items or magic spells.",
                    "Lunky: You did talk to everyone in the rest area and nugg koop? It would be awful if you missed a quest.",

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "erika_in_party": NpcTextBox(
                [
                    "Lunky: Certain dealers have magic points, if you leave their game they get back their MP",


                ],
                (50, 450, 50, 45), 30, 500
            ),
        }

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.character_sprite_image = pygame.image.load(
            "./assets/images/SNES - Harvest Moon - Carpenter.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):
        if self.state == "waiting":
            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":
            # Determine which message to use based on player state
            current_message = self.npc_messages["default_message"]
            if Events.ERIKA_IN_PARTY.value in state.player.companions:
                current_message = self.npc_messages["erika_in_party"]

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

        if (state.controller.isTPressed or state.controller.isAPressedSwitch) and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt((player.collision.x - self.collision.x) ** 2 + (player.collision.y - self.collision.y) ** 2)

            if distance < 40 and state.player.menu_paused == False:
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                # Reset the message based on player state
                current_message = self.npc_messages["default_message"]
                if Events.ERIKA_IN_PARTY.value in state.player.companions:
                    current_message = self.npc_messages["erika_in_party"]

                current_message.reset()

    def update_talking(self, state: "GameState", current_message):
        current_message.update(state)
        state.player.canMove = False

        if (state.controller.isTPressed or state.controller.isAPressedSwitch) and current_message.is_finished():
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            state.player.canMove = True

    def draw(self, state):
        # Draw character sprite
        sprite_rect = pygame.Rect(5, 6, 19, 25)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw the correct message box based on the state of the NPC

        if self.state == "talking":
            current_message = self.npc_messages["default_message"]
            if Events.ERIKA_IN_PARTY.value in state.player.companions:
                current_message = self.npc_messages["erika_in_party"]
            current_message.draw(state)

