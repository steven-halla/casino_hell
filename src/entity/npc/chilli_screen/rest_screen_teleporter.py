import math
import pygame
from entity.gui.textbox.text_box import TextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

class RestScreenFromChilliScreenTeleporter(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.selected_item_index = 0
        self.flipping_ted_messages = {
            "welcome_message": NpcTextBox(
                ["chili hog demon: You need to get prove yourself first. Go take down Ted, that ugly rat faced bastard has it coming.`"],
                (50, 450, 700, 130), 36, 500),
            "defeated_message": NpcTextBox(
                ["Good job on that take down, I was tired of looking at his ugly face. Hope Cindy's reward made you happy. Would you like to go to the rest area?You've earned it!"],
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
            "./assets/images/Game Boy Advance - Breath of Fire - Doof.png").convert_alpha()

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
            # Reset the message depending on the game state
            if state.coinFlipTedScreen.coinFlipTedDefeated:
                self.flipping_ted_messages["defeated_message"].reset()
            else:
                self.flipping_ted_messages["welcome_message"].reset()

    def update_talking(self, state: "GameState"):
        current_message = self.flipping_ted_messages["defeated_message"] if state.coinFlipTedScreen.coinFlipTedDefeated else self.flipping_ted_messages["welcome_message"]
        current_message.update(state)

        # Lock the player in place while talking



        # Check if the "T" key is pressed and the flag is not set
        if state.controller.isTPressed:
            print("Hi there you ")
            state.chili_area_to_rest_area_entry_point = True

            state.currentScreen = state.restScreen
            state.restScreen.start(state)
            # Handle the selected option
            selected_option = self.choices[self.arrow_index]
            print(f"Selected option: {selected_option}")

            # Check if the selected option is "Yes" and execute the code you provided




        if state.controller.isTPressed:
            # Exiting the conversation
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()

            # Unlock the player to allow movement
            # state.player.canMove = True

    def draw(self, state):
        pass