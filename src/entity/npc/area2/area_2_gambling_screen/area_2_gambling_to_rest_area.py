import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

class Area2GamblingToRestArea(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.selected_item_index = 0
        self.flipping_ted_messages = {
            "welcome_message": NpcTextBox(
                ["Gambling Guard: You need to get prove yourself first. Go take down Ted, that ugly rat faced bastard has it coming.`"],
                (50, 450, 700, 130), 36, 500),
            "defeated_message": NpcTextBox(
                ["Going to Gambling area"],
                (50, 450, 700, 130), 36, 500)
        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"
        self.flipping_ted_defeated = False
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.t_pressed = False


        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/Game Boy Advance - Breath of Fire - Doof.png").convert_alpha()

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
                (pygame.time.get_ticks() - self.state_start_time) > 500 and state.player.menu_paused == False:

            self.state_start_time = pygame.time.get_ticks()
            if state.controller.isTPressed:
                print("nannannnana")
                state.area_2_gambling_area_to_rest_point = True
                print(str(state.area_2_gambling_area_to_rest_point))

                state.currentScreen = state.area2RestScreen
                state.area2RestScreen.start(state)
            # Reset the message depending on the game state

    def update_talking(self, state: "GameState"):
        current_message = self.flipping_ted_messages["welcome_message"]
        current_message.update(state)

        # Lock the player in place while talking
        state.player.canMove = False





    def draw(self, state):


        if self.state == "talking":
            current_message = self.flipping_ted_messages["defeated_message"]
            current_message.draw(state)
