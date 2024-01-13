import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class ChillyBilly(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.queststart1 = NpcTextBox(
            ["ChillyBilly: I also want some water", "give me water and I'll reward you."],
            (50, 450, 50, 45), 30, 500)
        self.questfinish1 = NpcTextBox(
            ["ChillyBilly: Thanks for the hog of hedge I sure am hungry"],
            (50, 450, 50, 45), 30, 500)
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        self.textboxstate = "textbox1" # state = "textbox1" | "textbox2" | "textbox3" | "textbox4" | "textbox5"
        self.initialtalk = False
    def update(self, state: "GameState"):

        if self.state == "waiting":
            if "Nurgle the hedge hog" in state.player.items:
                self.textboxstate = "textbox2"

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
            if self.queststart1.message_index == 1:
                if state.controller.isAPressed and \
                        pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"

            elif self.questfinish1.message_index == 1:
                if state.controller.isAPressed and \
                        pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"

            elif "Nurgle the hedge hog" in state.player.items:
                print("Nurgle is here")


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
                if self.textboxstate == "textbox1":
                    print("Textbox1")
                    self.queststart1.reset()
                elif self.textboxstate == "textbox2":
                    print("Textbox2")
                    self.questfinish1.reset()

    def update_talking(self, state: "GameState"):
        self.queststart1.update(state)
        if state.controller.isTPressed and self.queststart1.is_finished():
            # if state.controller.isTPressed and self.textbox.message_index == 0:
            print("Here we go we're walking here")

            # print("start state: waiting")
            # self.textbox.reset()

            self.state = "waiting"

            self.state_start_time = pygame.time.get_ticks()
            # self.textbox.reset()
            print("now we are fin")
            self.initialtalk = True

            #this is where we want to set state to go to the next text box

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
            if self.textboxstate == "textbox1":
                self.queststart1.draw(state)
