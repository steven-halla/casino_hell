# import math
#
# import pygame
#
# from entity.npc.npc import Npc
# from entity.gui.textbox.npc_text_box import NpcTextBox
#
#
# class BarKeepLowBody(Npc):
#     def __init__(self, x: int, y: int):
#         super().__init__(x, y)
#         self.textbox = NpcTextBox(
#             [
#                 "Justin: come back when you have 2300 coins, I'll give you a stat boost potion for your body. Then yOu'll be able to drink and eat here to replenish your magic and stamina",
#                 "The chilli is quiet strong,I'll give you access to teh chili pit, if you pay me 2000 coins. I'll even give you a body +1"
#                 ],
#             (50, 450, 50, 45), 30, 500)
#         self.choices = ["Yes", "No"]
#         self.menu_index = 0
#         self.input_time = pygame.time.get_ticks()
#         self.quest_checker = False
#
#         self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
#         self.state = "waiting"  # states = "waiting" | "talking" | "finished"
#
#         self.character_sprite_image = pygame.image.load(
#             "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Bartender.png").convert_alpha()
#
#     def update(self, state: "GameState"):
#
#
#         if self.state == "waiting":
#             player = state.player
#             self.update_waiting(state)
#
#         elif self.state == "talking":
#             if state.player.money >= 2300 and self.quest_checker == False:
#                 state.player.body += 1
#                 state.player.mone -= 2000
#                 print("your body is now stronger check it out")
#                 print("no take backs I just sent the money. Now you can drink.")
#                 self.quest_checker = True
#                 return
#
#
#
#             if self.textbox.message_index == 1:
#                 if state.controller.isAPressed and \
#                         pygame.time.get_ticks() - self.input_time > 500:
#                     self.input_time = pygame.time.get_ticks()
#                     self.state = "waiting"
#
#                     state.player.money -= 100
#                     state.player.stamina_points += 500
#                     if state.player.stamina_points > 100:
#                         state.player.stamina_points = 100
#                 elif state.controller.isBPressed and \
#                         pygame.time.get_ticks() - self.input_time > 500:
#                     self.input_time = pygame.time.get_ticks()
#                     self.state = "waiting"
#
#             self.update_talking(state)
#
#     def update_waiting(self, state: "GameState"):
#         player = state.player
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
#
#             if distance < 40:
#                 self.state = "talking"
#                 self.state_start_time = pygame.time.get_ticks()
#                 self.textbox.reset()
#
#     def update_talking(self, state: "GameState"):
#         self.textbox.update(state)
#         state.player.canMove = False
#
#         if state.controller.isTPressed and self.textbox.is_finished():
#             self.state = "waiting"
#
#             self.state_start_time = pygame.time.get_ticks()
#             state.player.canMove = True
#
#     def draw(self, state):
#         sprite_rect = pygame.Rect(5, 6, 23, 30)
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
#         # rect = (
#         # self.collision.x + state.camera.x, self.collision.y + state.camera.y,
#         # self.collision.width, self.collision.height)
#         # pygame.draw.rect(state.DISPLAY, self.color, rect)
#
#         if self.state == "waiting":
#             pass
#         elif self.state == "talking":
#             # print("is talking")
#             self.textbox.draw(state)
import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class BarKeepLowBody(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        self.guy_messages = {
            "default_message": NpcTextBox(
                [
                    "Justin:Come back when you have 2000 coins, you can quit a match and go rest if you feel it too much.",

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "rabies_message": NpcTextBox(
                ["Bro, you look totally sick, go see the doctor ASAP"],
                (50, 450, 700, 130), 36, 500
            ),
        }

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Bartender.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):
        if self.state == "waiting":
            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":
            # Determine which message to use based on player state
            if state.player.money >= 2300 and self.quest_checker == False:
                state.player.body += 1
                state.player.mone -= 2000
                print("your body is now stronger check it out")
                print("no take backs I just sent the money. Now you can drink.")
                self.quest_checker = True
                return

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

