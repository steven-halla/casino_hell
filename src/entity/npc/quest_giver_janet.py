
import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

#### NOTE: BOTH JANET AND BILLY BOTH NEED HEDGE HOG AND WATER WILL NEED TO CHANGE IN FUTURE
####
####
class QuestGiverJanet(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.quest1giving = NpcTextBox(
            ["Hi there, I have some quest for you. Your first quest is easy : I want a bottle of water",
             "You should be able to find it in an treasure chest. Come back when you find it."],
            (50, 450, 50, 45), 30, 500)
        self.quest1completed = NpcTextBox(
            ["Oh you, giving me water, thank you so much I'll take that, are you sure? Fresh water is so rare down here",
             "I suppose you want a reward now. i'll teach you a new technique you can use for black jack."],
            (50, 450, 50, 45), 30, 500)
        self.quest2giving = NpcTextBox(
            ["IT's such a good thing you got me that water, you have no idea how good this tate.",
             "For future ref completing quest can net you other benifits such as increasing freindship with that person ."],
            (50, 450, 50, 45), 30, 500)
        self.quest2completed = NpcTextBox(
            ["Thank you so much for finding my friend",
             "now we can drink together, that is until the demons catch him again."],
            (50, 450, 50, 45), 30, 500)
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.reward1recieved = False
        self.reward2recieved = False
        self.quest2state = False
        self.quest3state = False

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):


        if self.state == "waiting":
  
            if "Nurgle the hedge hog" in state.player.items:
                if self.quest3state == False:
                    self.quest3state = True



            player = state.player

            min_distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)


            self.update_waiting(state)

        elif self.state == "talking":



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
                # if self.quest3state == True:
                #     self.quest2completed.reset()
                if self.quest2state == True:
                    self.quest2giving.reset()
                if self.reward1recieved and not self.quest2state:
                    self.quest2state = True
                    self.quest2giving.reset()
                if self.reward2recieved and not self.quest2state:
                    self.quest2state = True
                    self.quest2giving.reset()
                # the below is where kenny had it
                if self.reward1recieved == True:
                    self.quest1completed.reset()
                elif self.reward1recieved == False:
                    self.quest1giving.reset()


                # elif self.quest2state == True:
                #     self.quest2giving.reset()

    def update_talking(self, state: "GameState"):

        if self.reward1recieved == True:
            if "black jack spell" not in state.player.magicinventory:

                state.player.magicinventory.append("black jack spell")
            self.quest1completed.update(state)
            # if self.quest1completed.is_finished():
            #     self.quest2state = True
            #     print("quest 2 state is now: " + str(self.quest2state))

        if self.reward1recieved == False:
            self.quest1giving.update(state)
        if self.quest2state == True:
            self.quest2giving.update(state)

        # if self.quest3state == True:
        #     print("hey there hedge hog boy")
        #     self.quest2completed.update(state)

        # if self.quest3state == True and "Nurgle the hedge hog" in state.player.items:
            # print("this should be full" + str(state.player.items))

            # state.player.items.remove("Nurgle the hedge hog")
            # print("this should be empty" + str(state.player.items))

            # Reset quest1completed when the reward is first received
            # self.quest2completed.reset()

        if "Water Bottle" in state.player.items and not self.reward1recieved:
            self.reward1recieved = True
            print("Kool, you passed my quest!")
            print("this should be full" + str(state.player.items))

            state.player.items.remove("Water Bottle")
            print("this should be empty" + str(state.player.items))

            # Reset quest1completed when the reward is first received
            self.quest1completed.reset()

        if state.controller.isTPressed and self.quest2completed.is_finished():
            # if state.controller.isTPressed and self.textbox.message_index == 0:
            # print("Here we go we're walking here")

            # print("start state: waiting")
            # self.textbox.reset()

            self.state = "waiting"

            self.state_start_time = pygame.time.get_ticks()


        if state.controller.isTPressed and self.quest1giving.is_finished():
            # if state.controller.isTPressed and self.textbox.message_index == 0:
            # print("Here we go we're walking here")

            # print("start state: waiting")
            # self.textbox.reset()

            self.state = "waiting"

            self.state_start_time = pygame.time.get_ticks()
        if state.controller.isTPressed and self.quest1completed.is_finished():
            # if state.controller.isTPressed and self.textbox.message_index == 0:
            # print("Here we go we're walking here")

            # print("start state: waiting")
            # self.textbox.reset()

            self.state = "waiting"

            self.state_start_time = pygame.time.get_ticks()

        if state.controller.isTPressed and self.quest2giving.is_finished():
            # if state.controller.isTPressed and self.textbox.message_index == 0:
            # print("Here we go we're walking here")

            # print("start state: waiting")
            # self.textbox.reset()

            self.state = "waiting"

            self.state_start_time = pygame.time.get_ticks()
            # self.quest2state = True
            # print("quest 2 state is now here:" + str(self.quest2state))

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

            if self.quest3state == True:
                print("are we drawing this?")
                self.quest2completed.draw(state)
            elif self.reward1recieved == True and self.quest2state == False:
                self.quest1completed.draw(state)
            elif self.reward1recieved == False and self.quest2state == False:
                self.quest1giving.draw(state)
            elif self.quest2state == True:
                self.quest2giving.draw(state)




