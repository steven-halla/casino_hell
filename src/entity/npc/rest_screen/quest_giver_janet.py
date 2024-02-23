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
        self.queststart1 = NpcTextBox(
            ["I have a quest for you, get a score of 300 in opossum in a can from Nelly, Sandy, or Ichi", "These are the three people here you can do this from, be sure to complete the quest beforehand. Once you defeate someone you cant fight them."],
            (50, 450, 50, 45), 30, 500)
        self.questfinish1 = NpcTextBox(
            ["Janet: Good job on your bravery now take this reward, the new super special techniq that i learned from the dance floor:: Shake"],
            (50, 450, 50, 45), 30, 500)
        self.queststart2 = NpcTextBox(
            ["Janet: Come talk to me when you have the spell 'shield' "],
            (50, 450, 50, 45), 30, 500)
        self.questfinish2 = NpcTextBox(
            ["Janet: I'll give you something else, coin flip glasses.!"],
            (50, 450, 50, 45), 30, 500)
        self.queststart3 = NpcTextBox(
            ["Janet: Can you find my hedge hog friend Nurgle? We just seperated right before you talked to me. ",  "He loves to dig around in the trash, he's so cute, plump, white, looks very sickly, just make sure your perception is high or you wont find him"],
            (50, 450, 50, 45), 30, 500)

        self.questfinish3 = NpcTextBox(
            ["Janet:Thank you so much for finding my drinking buddy, hope you enjoy the extra magic stamina. ", "with a body of 1 you can drink with me."],
            (50, 450, 50, 45), 30, 500)
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        self.textboxstate = "textbox1" # state = "textbox1" | "textbox2" | "textbox3" | "textbox4" | "textbox5"
        self.talkfirstfivehundred = False
        self.quest2counter = False
        self.quest3counter = False
        self.find_hog = False
        self.level3reward = True

        self.path3 = False
        self.final_message_check = False

        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Eve.png").convert_alpha()

    def update(self, state: "GameState"):
        if "shake" in state.player.magicinventory:
            self.textboxstate = "textbox3"

        if state.player.spirit > 0 and "shake" in state.player.magicinventory and "Nurgle the hedge hog" not in state.player.items:
            self.textboxstate = "textbox5"

        if state.player.level3janetreward == True or "Nurgle the hedge hog" in state.player.items:
            self.textboxstate = "textbox6"
        # if state.restScreen.npc_janet_textbox3 == True:
        #     self.textboxstate = "textbox3"


        if state.restScreen.npc_janet_textbox2 == True:

            self.textboxstate = "textbox2"


        elif state.restScreen.npc_janet_textbox3 and state.player.spirit < 1:
            self.textboxstate = "textbox3"

        elif state.restScreen.npc_janet_textbox4 == True:
            self.textboxstate = "textbox4"

        elif state.restScreen.npc_janet_textbox5 == True and "Nurgle the hedge hog" not in state.player.items:
            self.textboxstate = "textbox5"


        elif state.restScreen.npc_janet_textbox6 == True and state.restScreen.rest_screen_npc_janet_find_hog == True:
            self.textboxstate = "textbox6"



        if self.state == "waiting":
            if state.gamblingAreaScreen.five_hundred_opossums == True and "shake" not in state.player.magicinventory:
                self.textboxstate = "textbox2"
                self.talkfirstfivehundred = False
                state.restScreen.npc_janet_textbox2 = True
                # print("am I getting reset?")
                # if self.talkfirstfivehundred == True:
                #     print("fjasd;fjkdls")


            if state.player.spirit == 1 and "coin flip glasses" not in state.player.items and "shake" in state.player.magicinventory:
                # print("time for the 2nd quest")
                self.textboxstate = "textbox4"
                self.find_hog = True
                state.restScreen.npc_janet_textbox4 = True


            if "Nurgle the hedge hog" in state.player.items and self.quest3counter == True:
                self.textboxstate = "textbox6"
                state.restScreen.npc_janet_textbox6 = True


            player = state.player

            # print("waiting")
            # if value is below 88 it wont activate for some reason
            min_distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)

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

            if distance < 70:
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
                    print("hi there text box 5 line 200")
                    state.restScreen.nurgle_the_hedge_hog = True
                    print("The rest screeen hog from janet class is: " + str(state.restScreen.nurgle_the_hedge_hog))
                elif self.textboxstate == "textbox6":
                    self.questfinish3.reset()

    def update_talking(self, state: "GameState"):
        current_time = pygame.time.get_ticks()

        state.player.canMove = False

        # Update and check the state of the appropriate text box
        if self.textboxstate == "textbox1":
            self.queststart1.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.queststart1.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    self.talkfirstfivehundred = True
                    state.player.canMove = True



        elif self.textboxstate == "textbox2":
            self.questfinish1.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                print("Hi")
                if self.questfinish1.is_finished():
                    # state.player.items.remove("Nurgle the hedge hog")
                    # if "janet reward 1" not in state.player.items:
                    #     state.player.items.append("janet reward 1")
                    print(self.textboxstate)

                    self.textboxstate = "textbox3"
                    print(state.player.magicinventory)
                    state.player.magicinventory.append("shake")
                    print(state.player.magicinventory)
                    self.path3 = True
                    state.restScreen.npc_janet_textbox3 = True
                    state.restScreen.npc_janet_textbox2 = False

                    print(self.textboxstate)

                    # self.talkfirstbeforehandoverhog = False

                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    print(self.textboxstate)
                    state.player.canMove = True




        elif self.textboxstate == "textbox3":
            print("am i here??????")

            self.queststart2.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.queststart2.is_finished():

                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    # self.talkfirstfivehundred = True
                    self.quest2counter = True
                    if "shield" in state.player.magicinventory:
                        state.restScreen.npc_janet_textbox4 = True
                        state.restScreen.npc_janet_textbox3 = False
                    elif state.player.spirit < 1:
                        state.restScreen.npc_janet_textbox4 = False
                        state.restScreen.npc_janet_textbox3 = True
                    state.player.canMove = True





        elif self.textboxstate == "textbox4":
            self.questfinish2.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.questfinish2.is_finished():
                    # state.player.items.remove("Water Bottle")
                    print("we are in textbox4")
                    self.quest2counter = False

                    print(state.player.items)
                    state.player.items.append("coin flip glasses")
                    print(state.player.magicinventory)
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    self.textboxstate = "textbox5"
                    state.restScreen.npc_janet_textbox5 = True
                    state.restScreen.npc_janet_textbox4 = False
                    state.player.canMove = True


        elif self.textboxstate == "textbox5":
            self.queststart3.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.queststart3.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    self.find_hog = True
                    self.quest3counter = True
                    state.gamblingAreaScreen.nurgle_the_hedge_hog = True
                    state.restScreen.npc_janet_textbox5 = False
                    state.restScreen.npc_janet_textbox6 = True
                    state.player.canMove = True


        elif self.textboxstate == "textbox6":
            self.questfinish3.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.questfinish3.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
                    if self.level3reward == True:
                        state.player.max_focus_points += 10
                        state.player.level3janetreward = True
                        self.level3reward = False


                    print("player body" + str(state.player.body))
                    self.find_hog = True
                    self.quest3counter = True
                    if "Nurgle the hedge hog" in state.player.items:
                        state.player.items.remove("Nurgle the hedge hog")
                    state.restScreen.nurgle_found = True
                    state.player.canMove = True

    def draw(self, state):
        sprite_rect = pygame.Rect(5, 6, 20, 25)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        if state.restScreen.bar_keeper_talking == False:
            state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

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
                self.find_hog = True
            elif self.textboxstate == "textbox6":
                self.questfinish3.draw(state)
                self.find_hog = True

