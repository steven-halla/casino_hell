import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class FlippingSandy(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.guy_messages = {
            "default_message": NpcTextBox(
                [
                    "Jessica: No more chili please god not again no no no no no no no no no no no no no god no please no anything but chili please somebody help me!",
                    "Hero: (These demons are just too cruel, hold on, I'll help you all.)"
                ],
                (50, 450, 50, 45), 30, 500
            ),

            "sir_leopold_message": NpcTextBox(
                ["I miss my girl friend Cindy. They keep making me drink beer till I'm about to pop."],
                (50, 450, 700, 130), 36, 500
            ),
        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

        self.character_sprite_image = pygame.image.load(
            "./assets/images/horse.png").convert_alpha()

    def update(self, state: "GameState"):
        if self.state == "waiting":
            # state.player.canMove = True

            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":


            # Determine which message to use based on player state
            current_message = self.guy_messages["default_message"]
            if "sir leopold" in state.player.companions:
                current_message = self.guy_messages["sir_leopold_message"]


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
                state.player.canMove = False


                self.state_start_time = pygame.time.get_ticks()
                # Reset the message based on player state
                current_message = self.guy_messages["default_message"]
                if "sir leopold" in state.player.companions:
                    current_message = self.guy_messages["sir_leopold_message"]
                current_message.reset()

    def update_talking(self, state: "GameState", current_message):
        current_message.update(state)

        if state.controller.isTPressed and current_message.is_finished():
            self.state = "waiting"
            state.player.canMove = True

            self.state_start_time = pygame.time.get_ticks()
    def draw(self, state):
        # rect = (
        # self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        # self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)


        sprite_rect = pygame.Rect(1, 80, 31, 28)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (60, 60))
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        if self.state == "talking":
            current_message =  self.guy_messages["default_message"]
            if "sir leopold" in state.player.companions:
                current_message = self.guy_messages["sir_leopold_message"]
            current_message.draw(state)
