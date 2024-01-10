
from constants import GREEN, BLUE
from entity.npc.npc import Npc
import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
font = pygame.font.Font('freesansbold.ttf', 24)

class CoinFlipFred(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.textbox = NpcTextBox([
            "You need at least 50 Hell coins to play",
            "Did you hear I use a weighted coin? It's a lie.",
            "Press the T key in order to start a battle with me."
        ], (50, 450, 50, 45), 30, 500)

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished" | "game_start

    def update(self, state: "GameState"):

        if self.state == "waiting":
            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":
            print("distance here")

            if state.controller.isAPressed:
                print("Hi A here")
                state.currentScreen = state.coinFlipTedScreen
                state.coinFlipTedScreen.start(state)

            if self.textbox.message_index == 1:
                print("talking")
                if state.controller.isAPressed and \
                        pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"


                elif state.controller.isBPressed and \
                        pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"

            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        min_distance = math.sqrt(
            (player.collision.x - self.collision.x) ** 2 + (
                        player.collision.y - self.collision.y) ** 2)

        if min_distance < 10:
            print("nooo")

        if state.controller.isTPressed and (
                pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)

            if distance < 40:
                self.state = "talking"

                self.state_start_time = pygame.time.get_ticks()
                self.textbox.reset()


    def update_talking(self, state: "GameState"):
        self.textbox.update(state)
        if state.controller.isTPressed and self.textbox.is_finished():
            self.state = "waiting"

            self.state_start_time = pygame.time.get_ticks()

    def draw(self, state):
        rect = (
            self.collision.x + state.camera.x, self.collision.y + state.camera.y,
            self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "waiting":
            pass
        elif self.state == "talking":

            # print("is talking")
            self.textbox.draw(state)