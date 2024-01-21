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
                    "Cindy: Cheating Ted is such a bastard. Because of him my boyfriend is making beer.",
                    "If you can take all his coins I'll reward you with a black jack technique. Pay attention to what his coins land on the most",
                    "The key to winning is to pay attention to patterns, which can change in the middle of playing",
                    "Try betting low, and get  a hang for the patterns before you go in for the kill."
                ],
                (50, 450, 50, 45), 30, 500
            ),
            'reward_message': NpcTextBox(
                [
                    "",
                    "Cindy: Oh kool look at you, time for your reward (inn badge). Oh, you want something else too, what a greedy man you are!.",
                    "Ok I know just what you want.....I'll give you this potion bottoms up!",
                    "Hero: Glug Glug Glug. Whoa....I feel, like, totally smarter! +1 MIND, 1st spell slot unlocked",
                    "Cindy: Thats not all, I'll also teach you a super secreat black jack technique passed down through generations of my family.",
                    "Now because your smarter you can count cards and get a  good sense of what your opponet has.",
                    "Black Jack Technique Reveal learned. Get a good sense of what your opponent has.",
                    "low: 1-9, med 10=15, high 16-21",

                ],

                (50, 450, 50, 45), 30, 500
            ),
            'final_message': NpcTextBox(
                [
                    "",
                    "Cindy: Watching you take him down was so satisfying thank you.",
                    "Black Jack Technique Reveal: Get a good sense of what your opponent has.",
                    "low: 1-9, med 10=15, high 16-21",
                ],
                (50, 450, 50, 45), 30, 500
            ),
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
        if state.coinFlipTedScreen.coinFlipTedDefeated and "inn badge" not in state.player.items:
            state.player.items.append("inn badge")
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
        if self.coinFlipTedReward == True:
            current_message = self.cindy_long_hair_messages['final_message']
        elif state.coinFlipTedScreen.coinFlipTedDefeated:
            current_message = self.cindy_long_hair_messages['reward_message']
        else:
            current_message = self.cindy_long_hair_messages['textbox']
        current_message.update(state)
        if state.controller.isTPressed and current_message.is_finished():
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            current_message.reset()  # Ensure the message is reset for the next interaction
            if "black jack reveal" in state.player.magicinventory:
                self.coinFlipTedReward = True


    def draw(self, state):
        rect = (
            self.collision.x + state.camera.x, self.collision.y + state.camera.y,
            self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "talking":
            if self.coinFlipTedReward == True:
                current_message = self.cindy_long_hair_messages['final_message']
            elif state.coinFlipTedScreen.coinFlipTedDefeated:
                current_message = self.cindy_long_hair_messages['reward_message']
            else:
                current_message = self.cindy_long_hair_messages['textbox']
            current_message.draw(state)
            while state.coinFlipTedScreen.coinFlipTedDefeated == True and "black jack reveal" not in state.player.magicinventory:
                state.player.mind += 1
                state.player.magicinventory.append("black jack reveal")
                print(state.player.magicinventory)
                print(state.player.mind)
                # self.coinFlipTedReward = True

                return



