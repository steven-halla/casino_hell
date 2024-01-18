import math
import pygame
from entity.gui.textbox.text_box import TextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

class FlippinTed(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.flipping_ted_messages = {
            "welcome_message": NpcTextBox(
                ["Press T to select options and go through T messages, press  A to play", "Welcome to Coin flip I'll make you flip!"],
                (50, 450, 700, 130), 36, 500),
            "defeated_message": NpcTextBox(
                ["Looks like you defeated me, how sad :("],
                (50, 450, 700, 130), 36, 500)
        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"

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

        # Logic for entering the game by pressing the 'A' button
        if state.controller.isAPressed and not state.coinFlipTedScreen.coinFlipTedDefeated:
            state.currentScreen = state.coinFlipTedScreen
            state.coinFlipTedScreen.start(state)

        if state.controller.isTPressed and current_message.is_finished():
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()

    def draw(self, state):
        rect = (self.collision.x + state.camera.x, self.collision.y + state.camera.y, self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "talking":
            current_message = self.flipping_ted_messages["defeated_message"] if state.coinFlipTedScreen.coinFlipTedDefeated else self.flipping_ted_messages["welcome_message"]
            current_message.draw(state)




