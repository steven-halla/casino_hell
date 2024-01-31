import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


#### NOTE: BOTH JANET AND BILLY BOTH NEED HEDGE HOG AND WATER WILL NEED TO CHANGE IN FUTURE
####
####
class ChillyBilly(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.queststart1 = NpcTextBox(
            ["ChillyBilly: I made this batch of chilli myself. Don't forget to eat it with your bare hands.",
             "Hero: With our bare hands? No spoons or bowls? Isn't that kind of.....eating it like an animal?",
             "ChillyBilly: To us, eating chilli wiht a spoon and bowl is like to you humans going to a fancy restaruant.",
             "And eating a fancy dinner in the toilet. It's rather insulting to the cook. So don't insult us and use your bare hands to eat that chilli.",
             ],
            (50, 450, 50, 45), 30, 500)
        self.questfinish1 = NpcTextBox(
            ["ChillyBilly: Thanks for the hog of hedge I sure am hungry"],
            (50, 450, 50, 45), 30, 500)
        self.queststart2 = NpcTextBox(
            ["ChillyBilly: I have a new quest for you. Find me some water please"],
            (50, 450, 50, 45), 30, 500)
        self.questfinish2 = NpcTextBox(
            ["ChillyBilly: Oh wow this is water thank you!"],
            (50, 450, 50, 45), 30, 500)
        self.queststart3 = NpcTextBox(
            ["ChillyBilly: in the future you'll need to defeat two opponets "],
            (50, 450, 50, 45), 30, 500)
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        self.textboxstate = "textbox1" # state = "textbox1" | "textbox2" | "textbox3" | "textbox4" | "textbox5"
        self.talkfirstbeforehandoverhog = False
        self.talkfirstbeforehandoverwater = False


        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/Game Boy Advance - Breath of Fire - Doof.png").convert_alpha()

    def update(self, state: "GameState"):

        if self.state == "waiting":
            if "Nurgle the hedge hog" in state.player.items and self.talkfirstbeforehandoverhog == True:

                self.textboxstate = "textbox2"
                print(self.textboxstate)

            if "Water Bottle" in state.player.items and self.talkfirstbeforehandoverwater == True:
                self.textboxstate = "textbox4"
                print(self.textboxstate)

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
                # print("10")

                self.state = "talking"

                self.state_start_time = pygame.time.get_ticks()
                # the below is where kenny had it
                if self.textboxstate == "textbox1":
                    # print("Textbox1")
                    self.queststart1.reset()
                elif self.textboxstate == "textbox2":
                    # print("Textbox2")
                    self.questfinish1.reset()
                elif self.textboxstate == "textbox3":
                    self.queststart2.reset()
                elif self.textboxstate == "textbox4":
                    self.questfinish2.reset()
                elif self.textboxstate == "textbox5":
                    self.queststart3.reset()

    def update_talking(self, state: "GameState"):
        current_time = pygame.time.get_ticks()

        # Update and check the state of the appropriate text box
        if self.textboxstate == "textbox1":
            self.queststart1.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.queststart1.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    self.talkfirstbeforehandoverhog = True


        elif self.textboxstate == "textbox2":
            self.questfinish1.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.questfinish1.is_finished():
                    state.player.items.remove("Nurgle the hedge hog")

                    self.textboxstate = "textbox3"
                    # self.talkfirstbeforehandoverhog = False

                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time


        elif self.textboxstate == "textbox3":
            self.queststart2.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.queststart2.is_finished():

                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    self.talkfirstbeforehandoverwater = True



        elif self.textboxstate == "textbox4":
            self.questfinish2.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.questfinish2.is_finished():
                    state.player.items.remove("Water Bottle")


                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    self.textboxstate = "textbox5"

        elif self.textboxstate == "textbox5":
            self.queststart3.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.queststart3.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time



    def draw(self, state):
        sprite_rect = pygame.Rect(5, 6, 24, 28)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))
        # rect = (
        # self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        # self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "waiting":
            pass
        elif self.state == "talking":
            # print("is talking")
            if self.textboxstate == "textbox1":
                self.queststart1.draw(state)
            elif self.textboxstate == "textbox2":
                self.questfinish1.draw(state)
            elif self.textboxstate == "textbox3":
                self.queststart2.draw(state)
            elif self.textboxstate == "textbox4":
                self.questfinish2.draw(state)
            elif self.textboxstate == "textbox5":
                self.queststart3.draw(state)
