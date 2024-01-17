import math
import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class CindyLongHair(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.cindy_long_hair_messages = {
            'textbox': NpcTextBox(
                [
                    "Cindy: Cheating Ted is such a jerk. If you could take all of his coins I'll reward you.",
                    "Most of his coin flips land on tails, he trained himself to do that.",
                    "Hero: So against him I should bet tails, most people tend to bet 'heads', very smart of him to know that much."
                ],
                (50, 450, 50, 45), 30, 500
            ),
            'reward_message': NpcTextBox(
                [
                    "",
                    "Cindy: Oh kool look at you, time for your reward *smooch*. Oh, you want something else too, what a greedy man you are, take it and good luck!."
                ],
                (50, 450, 50, 45), 30, 500
            )
        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.coinFlipTedReward = False

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        min_distance = math.sqrt(
            (player.collision.x - self.collision.x) ** 2 + (
                        player.collision.y - self.collision.y) ** 2)
        if min_distance < 10:
            print("nooo")

        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            if distance < 40:
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                self.cindy_long_hair_messages['textbox'].reset()

    def update_talking(self, state: "GameState"):
        current_message = self.cindy_long_hair_messages['reward_message'] if state.coinFlipTedScreen.coinFlipTedDefeated else self.cindy_long_hair_messages['textbox']
        current_message.update(state)
        if state.controller.isTPressed and current_message.is_finished():
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            current_message.reset()  # Ensure the message is reset for the next interaction

    def draw(self, state):
        rect = (
            self.collision.x + state.camera.x, self.collision.y + state.camera.y,
            self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "talking":
            current_message = self.cindy_long_hair_messages['reward_message'] if state.coinFlipTedScreen.coinFlipTedDefeated else self.cindy_long_hair_messages['textbox']
            current_message.draw(state)
