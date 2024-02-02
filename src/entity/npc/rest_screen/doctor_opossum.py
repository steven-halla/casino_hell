import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class DoctorOpossum(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.doctor_messages = {
            "welcome_message": NpcTextBox(
                ["I'm a rabies doctor, i used to be a heart surgeon", "If you need any help in the future let me know", "Hero: If i need to swing by I will"],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "rabies_message": NpcTextBox(
                ["Sorry to hear you have rabies......go to the hedge maze and look for a bottle of water"],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),
            "cured_message": NpcTextBox(
                ["thank you for the flower....i'll cure you...and here, so you take less damaege! Now go and rest up at the Inn, Doctor's orders!!! "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),

            "sir_leopold_message": NpcTextBox(
                ["You have a companion...now he'll be safe!, As long as you have  money.... "],
                (50, 450, 700, 130),  # Position and size
                36,  # Font size
                500  # Delay
            ),

            # You can add more game state keys and TextBox instances here
        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.hero_rabies = False

        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Eve.png").convert_alpha()


        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):
        # print(state.restScreen.chili_pit_flag)

        if state.player.hasRabies == True:
            self.hero_rabies = True




        ###my current idea is to have one more state: blue flower, and have that

        ###,maybe will have to wait and see though
        ###
        ###

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

            if state.player.hasRabies == True:
                state.restScreen.chili_pit_flag = True


            # self.textbox.reset()
            # self.textbox.message_index = 0

            if "sir leopold" in state.player.companions:
                if self.doctor_messages["sir_leopold_message"].message_index == 1:
                    if state.controller.isAPressed and \
                            pygame.time.get_ticks() - self.input_time > 500:
                        self.input_time = pygame.time.get_ticks()
                        self.state = "waiting"


                    elif state.controller.isBPressed and \
                            pygame.time.get_ticks() - self.input_time > 500:
                        self.input_time = pygame.time.get_ticks()
                        print("bye player")
                        self.state = "waiting"


            elif "blue flower" in state.player.items:
                if self.doctor_messages["cured_message"].message_index == 1:

                    if state.controller.isAPressed and \
                            pygame.time.get_ticks() - self.input_time > 500:
                        self.input_time = pygame.time.get_ticks()
                        self.state = "waiting"


                    elif state.controller.isBPressed and \
                            pygame.time.get_ticks() - self.input_time > 500:
                        self.input_time = pygame.time.get_ticks()
                        print("bye player")
                        self.state = "waiting"

            elif self.hero_rabies == False:
                if self.doctor_messages["welcome_message"].message_index == 1:
                    if state.controller.isAPressed and \
                            pygame.time.get_ticks() - self.input_time > 500:
                        self.input_time = pygame.time.get_ticks()
                        self.state = "waiting"


                    elif state.controller.isBPressed and \
                            pygame.time.get_ticks() - self.input_time > 500:
                        self.input_time = pygame.time.get_ticks()
                        print("bye player")
                        self.state = "waiting"

            elif self.hero_rabies == True:
                if self.doctor_messages["rabies_message"].message_index == 1:
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

                self.state = "talking"

                self.state_start_time = pygame.time.get_ticks()

                if "sir leopold" in state.player.companions:
                    self.doctor_messages["sir_leopold_message"].reset()


                elif "blue flower" in state.player.items or state.player.rabiesImmunity == True:
                    self.doctor_messages["cured_message"].reset()
                    # state.player.hasRabies = False

                elif self.hero_rabies == False:
                # the below is where kenny had it
                    self.doctor_messages["welcome_message"].reset()
                elif self.hero_rabies == True:
                    self.doctor_messages["rabies_message"].reset()


    def update_talking(self, state: "GameState"):
        state.player.canMove = False

        if "sir leopold" in state.player.companions:
            self.doctor_messages["sir_leopold_message"].update(state)
            if state.controller.isTPressed and self.doctor_messages["sir_leopold_message"].is_finished():
                # if state.controller.isTPressed and self.textbox.message_index == 0:
                print("Here we go we're walking here")

                self.state = "waiting"

                self.state_start_time = pygame.time.get_ticks()
                state.player.canMove = True



        elif "blue flower" in state.player.items:
            self.doctor_messages["cured_message"].update(state)
            if state.controller.isTPressed and self.doctor_messages["cured_message"].is_finished():
                # if state.controller.isTPressed and self.textbox.message_index == 0:
                print("Here we go we're walking here")
                # state.player.items.append("opossum repellent")
                state.player.hasRabies = False

                state.player.rabiesImmunity = True
                state.player.items.remove("blue flower")

                # print("start state: waiting")
                # self.textbox.reset()

                self.state = "waiting"

                self.state_start_time = pygame.time.get_ticks()
                state.player.canMove = True


        elif self.hero_rabies == False:
            self.doctor_messages["welcome_message"].update(state)
            if state.controller.isTPressed and self.doctor_messages["welcome_message"].is_finished():
                # if state.controller.isTPressed and self.textbox.message_index == 0:
                print("Here we go we're walking here")

                # print("start state: waiting")
                # self.textbox.reset()

                self.state = "waiting"

                self.state_start_time = pygame.time.get_ticks()
                state.player.canMove = True

        elif self.hero_rabies == True:
            self.doctor_messages["rabies_message"].update(state)
            if state.controller.isTPressed and self.doctor_messages["rabies_message"].is_finished():
                # if state.controller.isTPressed and self.textbox.message_index == 0:
                print("Here we go we're walking here")

                # print("start state: waiting")
                # self.textbox.reset()

                self.state = "waiting"

                self.state_start_time = pygame.time.get_ticks()
                state.player.canMove = True

            # self.textbox.reset()

    # def isOverlap(self, entity: "Entity") -> bool:
    #     print("Overlap called")
    #     return self.collision.isOverlap(entity.collision)

    def draw(self, state):
        # rect = (
        # self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        # self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)

        sprite_rect = pygame.Rect(194, 5, 18, 24)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        if self.state == "waiting":
            pass
        elif self.state == "talking":
            # print("is talking")
            #make a new message path

            if "sir leopold" in state.player.companions:
                self.doctor_messages["sir_leopold_message"].draw(state)

            elif "blue flower" in state.player.items:
                self.doctor_messages["cured_message"].draw(state)

            elif self.hero_rabies == False:
                self.doctor_messages["welcome_message"].draw(state)
            elif self.hero_rabies == True:
                self.doctor_messages["rabies_message"].draw(state)

