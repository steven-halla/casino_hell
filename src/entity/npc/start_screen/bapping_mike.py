import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class BappingMike(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.textbox = NpcTextBox(
            [
                "Mike: Money is FINITE, so don't waste it.",
                "You need money to buy items, gamble, and move on to the next area..",
                " ammass 2000 coins and  you can play the boss to advance.",
                "Also, the more you bet, the more stamina you lose, but you gain more EXP, you also gain EXP for losing",
                "down here on the 1st floor we all repeat outselves, sometimes the people in the rest area have something new to say",
                "You'll get a clue when that happens, so don't waste your time re talking to people all the time. Unless you want to go crazy like the others",
                "You can just look at the eyes an tell which ones are crazy, sometimes they just ramble on and on and on",
                "Like you would think people would know better than to ramble, but nope, not me I'm not a rambling Randy.",
                "What about you? Do you like to ramble? Your not saying much, you must be rambling to yourself, yeah, your rambling."],
            (50, 450, 50, 45), 30, 500)
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):

        if self.state == "waiting":
            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":

            # if state.player.money > 1300:
            if self.textbox.message_index == len(
                    self.textbox.messages) - 1 and state.player.money >= 1300:
                print("Last message has been displayed")

                state.player.inn_badge = True

            if self.textbox.message_index == 1:
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
