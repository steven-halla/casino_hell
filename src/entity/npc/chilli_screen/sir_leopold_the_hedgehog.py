import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

##
##sir leopold should block exit till we talk to him post quests
##we will append sir leopold in front of entrance if player has flower
##
##
class SirLeopoldTheHedgeHog(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.textbox = NpcTextBox(
            ["I'm the head hog round these parts",
             "Oh hero wont you pretty please help my friends, they are hdiing out in the hedge maze, please help you'll get rewarded "],
            (50, 450, 50, 45), 30, 500)
        self.reward_no_hogs = NpcTextBox(
            ["wow you reall suckss",
             "Oh hero wont you pretty please help my friends, they are hdiing out in the hedge maze, please help you'll get rewarded "],
            (50, 450, 50, 45), 30, 500)
        self.reward_some_hogs = NpcTextBox(
            ["well at least you triedss",
             "Oh hero got some of dem hoggy hoggers out in the hedge maze, please help you'll get rewarded "],
            (50, 450, 50, 45), 30, 500)
        self.reward_all_hogs = NpcTextBox(
            ["you got em all great",
             "Oh hero wont you pretty please help my friends, they are hdiing out in the hedge maze, please help you'll get rewarded "],
            (50, 450, 50, 45), 30, 500)

        self.final_message = NpcTextBox(
            ["final message here from sir leopold",
             "Oh hero wont you pretty please help my friends, they are hdiing out in the hedge maze, please help you'll get rewarded "],
            (50, 450, 50, 45), 30, 500)

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.to_be_deleted = False  # Flag to mark the object for deletion
        self.textboxstate = "textbox1" # state = "textbox1" | "textbox2" | "textbox3" | "textbox4" | "textbox5"


        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):


        if self.state == "waiting":
            print("current state is:" + str(self.textboxstate))

            if state.hedgeMazeScreen.blue_flower == True:
                if state.hedgeMazeScreen.hedge_hog_counter == 0:
                    self.textboxstate = "textbox2"
                    print("no hoggy hogs for u")
                elif state.hedgeMazeScreen.hedge_hog_counter < 4:
                    self.textboxstate = "textbox3"
                elif state.hedgeMazeScreen.hedge_hog_counter == 4:
                    self.textboxstate = "textbox4"



                #     if self.reward_all_hogs.is_finished():
                #         # Transition to textboxstate 5 after reward_all_hogs is finished
                #         self.textboxstate = "textbox5"
                # elif self.textboxstate == "textbox5":
                    # self.final_message.update(state)





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
                if self.textboxstate == "textbox2":
                    # print("Textbox1")
                    self.reward_no_hogs.reset()
                elif self.textboxstate == "textbox3":
                    # print("Textbox1")
                    self.reward_some_hogs.reset()
                elif self.textboxstate == "textbox4":
                    # print("Textbox1")
                    self.reward_all_hogs.reset()
                elif self.textboxstate == "textbox1":
                    self.textbox.reset()
                elif self.textboxstate == "textbox5":
                    self.final_message.reset()



    def update_talking(self, state: "GameState"):

        current_time = pygame.time.get_ticks()


        if self.textboxstate == "textbox2":
            self.reward_no_hogs.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.reward_no_hogs.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
        elif self.textboxstate == "textbox3":
            self.reward_some_hogs.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.reward_some_hogs.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time
        elif self.textboxstate == "textbox4":
            self.reward_all_hogs.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.reward_all_hogs.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time

        elif self.textboxstate == "textbox1":
            self.textbox.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.textbox.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time
        elif self.textboxstate == "textbox5":
            self.final_message.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.final_message.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time


        if state.controller.isTPressed and self.textbox.is_finished():
            # if state.controller.isTPressed and self.textbox.message_index == 0:
            print("Here we go we're walking here")


            # print("start state: waiting")
            # self.textbox.reset()

            self.state = "waiting"
            # if "Nurgle the hedge hog" not in state.player.items:
            #     state.player.items.append("Nurgle the hedge hog")
            #     print("Added: " + str(state.player.items))

            self.state_start_time = pygame.time.get_ticks()
            self.to_be_deleted = True  # Mark the object for deletion

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
            if self.textboxstate == "textbox2":
                self.reward_no_hogs.draw(state)
            elif self.textboxstate == "textbox3":
                self.reward_some_hogs.draw(state)
            elif self.textboxstate == "textbox4":
                self.reward_all_hogs.draw(state)
            elif self.textboxstate == "textbox5":
                self.final_message.draw(state)
            elif self.textboxstate == "textbox1":
                self.textbox.draw(state)

