# import math
#
# import pygame
#
# from entity.npc.npc import Npc
# from entity.gui.textbox.npc_text_box import NpcTextBox
#
#
# class SufferingSuzy(Npc):
#     def __init__(self, x: int, y: int):
#         super().__init__(x, y)
#         self.textbox = NpcTextBox(
#             ["Suzy: If you have 3000 coins you can go to the next area",
#              "food can have unique effects depending on what you eat."],
#             (50, 450, 50, 45), 30, 500)
#         self.choices = ["Yes", "No"]
#         self.menu_index = 0
#         self.input_time = pygame.time.get_ticks()
#
#
#         self.character_sprite_image = pygame.image.load(
#             "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Seed Shop Owner.png").convert_alpha()
#
#         self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
#         self.state = "waiting"  # states = "waiting" | "talking" | "finished"
#
#     def update(self, state: "GameState"):
#
#         if self.state == "waiting":
#             player = state.player
#
#             # print("waiting")
#             # if value is below 88 it wont activate for some reason
#             min_distance = math.sqrt(
#                 (player.collision.x - self.collision.x) ** 2 + (
#                             player.collision.y - self.collision.y) ** 2)
#             #
#             # if min_distance < 25:
#             #     print("nooo")
#
#             self.update_waiting(state)
#
#         elif self.state == "talking":
#             # self.textbox.reset()
#             # self.textbox.message_index = 0
#             if self.textbox.message_index == 1:
#                 if state.controller.isAPressed and \
#                         pygame.time.get_ticks() - self.input_time > 500:
#                     self.input_time = pygame.time.get_ticks()
#                     self.state = "waiting"
#
#
#                 elif state.controller.isBPressed and \
#                         pygame.time.get_ticks() - self.input_time > 500:
#                     self.input_time = pygame.time.get_ticks()
#                     print("bye player")
#                     self.state = "waiting"
#
#             self.update_talking(state)
#
#     def update_waiting(self, state: "GameState"):
#         player = state.player
#         # print(self.state)
#         min_distance = math.sqrt(
#             (player.collision.x - self.collision.x) ** 2 + (
#                         player.collision.y - self.collision.y) ** 2)
#
#         if min_distance < 10:
#             print("nooo")
#
#         if state.controller.isTPressed and (
#                 pygame.time.get_ticks() - self.state_start_time) > 500:
#             distance = math.sqrt(
#                 (player.collision.x - self.collision.x) ** 2 + (
#                             player.collision.y - self.collision.y) ** 2)
#             # print("distance: " + str(distance))
#
#             if distance < 40:
#                 # print("start state: talking")
#                 print("10")
#
#                 self.state = "talking"
#
#                 self.state_start_time = pygame.time.get_ticks()
#                 # the below is where kenny had it
#                 self.textbox.reset()
#
#     def update_talking(self, state: "GameState"):
#         self.textbox.update(state)
#         state.player.canMove = False
#
#         if state.controller.isTPressed and self.textbox.is_finished():
#             # if state.controller.isTPressed and self.textbox.message_index == 0:
#             print("Here we go we're walking here")
#
#             # print("start state: waiting")
#             # self.textbox.reset()
#
#             self.state = "waiting"
#
#             self.state_start_time = pygame.time.get_ticks()
#             state.player.canMove = True
#
#
#             # self.textbox.reset()
#
#     # def isOverlap(self, entity: "Entity") -> bool:
#     #     print("Overlap called")
#     #     return self.collision.isOverlap(entity.collision)
#
#     def draw(self, state):
#         # rect = (
#         # self.collision.x + state.camera.x, self.collision.y + state.camera.y,
#         # self.collision.width, self.collision.height)
#         # pygame.draw.rect(state.DISPLAY, self.color, rect)
#
#         sprite_rect = pygame.Rect(5, 6, 18, 26)
#
#         # Get the subsurface for the area you want
#         sprite = self.character_sprite_image.subsurface(sprite_rect)
#
#         # Scale the subsurface to make it two times bigger
#         scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88
#
#         # Define the position where you want to draw the sprite
#         sprite_x = self.collision.x + state.camera.x - 20
#         sprite_y = self.collision.y + state.camera.y - 10
#
#         # Draw the scaled sprite portion on the display
#         state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))
#
#         if self.state == "waiting":
#             pass
#         elif self.state == "talking":
#             # print("is talking")
#             self.textbox.draw(state)
#

import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class SufferingSuzy(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        self.guy_messages = {
            "default_message": NpcTextBox(
                [
                    "Suzy: If you have 3000 coins you can go to the next area",
                    "food can have unique effects depending on what you eat."
                ],
                (50, 450, 50, 45), 30, 500
            ),
            "rabies_message": NpcTextBox(
                ["You look much cuter right now, I can't quiet put my finger on why..."],
                (50, 450, 700, 130), 36, 500
            ),
        }

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()


        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Seed Shop Owner.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):
        if self.state == "waiting":
            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":
            # Determine which message to use based on player state
            current_message = self.guy_messages["rabies_message"] if state.player.hasRabies else self.guy_messages["default_message"]

            if current_message.message_index == 1:
                if state.controller.isAPressed and pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"

                    state.player.money -= 100
                    state.player.stamina_points += 500
                    if state.player.stamina_points > 100:
                        state.player.stamina_points = 100
                elif state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"

            self.update_talking(state, current_message)

    def update_waiting(self, state: "GameState"):
        player = state.player
        min_distance = math.sqrt((player.collision.x - self.collision.x) ** 2 + (player.collision.y - self.collision.y) ** 2)

        if min_distance < 10:
            print("nooo")

        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt((player.collision.x - self.collision.x) ** 2 + (player.collision.y - self.collision.y) ** 2)

            if distance < 40:
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                # Reset the message based on player state
                current_message = self.guy_messages["rabies_message"] if state.player.hasRabies else self.guy_messages["default_message"]
                current_message.reset()

    def update_talking(self, state: "GameState", current_message):
        current_message.update(state)
        state.player.canMove = False

        if state.controller.isTPressed and current_message.is_finished():
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            state.player.canMove = True

    def draw(self, state):
        # Draw character sprite
        sprite_rect = pygame.Rect(7, 6, 17.5, 24)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw the correct message box based on the state of the NPC
        if self.state == "talking":
            current_message = self.guy_messages["rabies_message"] if state.player.hasRabies else self.guy_messages["default_message"]
            current_message.draw(state)

