import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class QuestGiverJanet(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.textbox = NpcTextBox(
            ["Hi there, I have some quest for you. Your first quest is easy : I want a bottle of water",
             "You should be able to find it in an treasure chest. Come back when you find it."],
            (50, 450, 50, 45), 30, 500)
        self.textboxwaterbottlegiven = NpcTextBox(
            ["Oh you, giving me water, thank you so much I'll take that, are you sure? Fresh water is so rare down here",
             "I suppose you want a reward now. i'll teach you a new technique you can use for black jack."],
            (50, 450, 50, 45), 30, 500)
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.reward1recieved = False

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):

        if self.state == "waiting":
            player = state.player

            # print("waiting")
            # if value is below 88 it wont activate for some reason
            min_distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            #
            # if min_distance < 25:
            #     print("nooo")

            self.update_waiting(state)

        elif self.state == "talking":
            # self.textbox.reset()
            # self.textbox.message_index = 0
            if self.reward1recieved == True:
                if self.textboxwaterbottlegiven.message_index == 1:
                    if state.controller.isAPressed and \
                            pygame.time.get_ticks() - self.input_time > 500:
                        self.input_time = pygame.time.get_ticks()
                        self.state = "waiting"
            elif self.reward1recieved == False:
                if self.textbox.message_index == 1:
                    if state.controller.isAPressed and \
                            pygame.time.get_ticks() - self.input_time > 500:
                        self.input_time = pygame.time.get_ticks()
                        self.state = "waiting"



                elif state.controller.isBPressed and \
                        pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    print("bye player")
                    self.state = "waiting"

            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        # print(self.state)
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
            # print("distance: " + str(distance))

            if distance < 40:
                # print("start state: talking")
                print("10")

                self.state = "talking"

                self.state_start_time = pygame.time.get_ticks()
                # the below is where kenny had it
                if self.reward1recieved == True:
                    self.textboxwaterbottlegiven.reset()
                elif self.reward1recieved == False:
                    self.textbox.reset()

    def update_talking(self, state: "GameState"):
        if self.reward1recieved == True:
            self.textboxwaterbottlegiven.update(state)
        elif self.reward1recieved == False:
            self.textbox.update(state)
        if "Water Bottle" in state.player.items and not self.reward1recieved:
            self.reward1recieved = True
            print("Kool, you passed my quest!")
            print("this should be full" + str(state.player.items))

            state.player.items.remove("Water Bottle")
            print("this should be empty" + str(state.player.items))

            # Reset textboxwaterbottlegiven when the reward is first received
            self.textboxwaterbottlegiven.reset()


        if state.controller.isTPressed and self.textbox.is_finished():
            # if state.controller.isTPressed and self.textbox.message_index == 0:
            # print("Here we go we're walking here")

            # print("start state: waiting")
            # self.textbox.reset()

            self.state = "waiting"

            self.state_start_time = pygame.time.get_ticks()
        if state.controller.isTPressed and self.textboxwaterbottlegiven.is_finished():
            # if state.controller.isTPressed and self.textbox.message_index == 0:
            # print("Here we go we're walking here")

            # print("start state: waiting")
            # self.textbox.reset()

            self.state = "waiting"

            self.state_start_time = pygame.time.get_ticks()
            # self.textbox.reset()

    # def isOverlap(self, entity: "Entity") -> bool:
    #     print("Overlap called")
    #     return self.collision.isOverlap(entity.collision)

    def draw(self, state):
        rect = (
        self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "waiting":
            pass
        elif self.state == "talking":
            # print("is talking")
            if self.reward1recieved == True:
                self.textboxwaterbottlegiven.draw(state)
            elif self.reward1recieved == False:
                self.textbox.draw(state)

