import math
import pygame
from entity.gui.textbox.text_box import TextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

class Amber(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.selected_item_index = 0
        self.black_jack_thomas_messages = {
            "welcome_message": NpcTextBox(
                ["Jack: Whatever you heard about me isn't true I swear it.  Wanna battle?"],
                (50, 450, 700, 130), 36, 500),
            "defeated_message": NpcTextBox(
                ["Jack That's the 100th time I've lost, I don't know why the demons keep giving me coins."],
                (50, 450, 700, 130), 36, 500),

            "rabies_message": NpcTextBox(
                ["Jack GET AWAY FROM ME YOU FROTHY MOUTHED BASTARD."],
                (50, 450, 700, 130), 36, 500),


        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"
        self.black_jack_thomas_defeated = False
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.t_pressed = False



        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Mayor.png").convert_alpha()

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        distance = math.sqrt((player.collision.x - self.collision.x) ** 2 +
                             (player.collision.y - self.collision.y) ** 2)

        if distance < 40 and state.controller.isTPressed and \
                (pygame.time.get_ticks() - self.state_start_time) > 500:
            self.state = "talking"
            self.state_start_time = pygame.time.get_ticks()


            self.black_jack_thomas_messages["welcome_message"].reset()

    def update_talking(self, state: "GameState"):
        current_message = (
           self.black_jack_thomas_messages["welcome_message"]

        )
        current_message.update(state)


        # Lock the player in place while talking
        state.player.canMove = False



        # Check if the "T" key is pressed and the flag is not set


        if state.controller.isTPressed and current_message.is_finished():
            state.controller.isTPressed = False
            # Exiting the conversation
            self.state = "waiting"
            self.menu_index = 0
            self.arrow_index = 0
            self.state_start_time = pygame.time.get_ticks()

            # Unlock the player to allow movement
            state.player.canMove = True

    def draw(self, state):
        # rect = (
        #     self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        #     self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)

        sprite_rect = pygame.Rect(7, 6, 16.4, 24)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        if self.state == "talking":
            current_message = (
              self.black_jack_thomas_messages["welcome_message"]

            )

            current_message.draw(state)

