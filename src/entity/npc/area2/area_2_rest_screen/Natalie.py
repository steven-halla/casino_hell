import math
import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.events import Events


class Natalie(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.npc_messages = {
            "default_message": NpcTextBox(
                [
                    "Natalie: Have you ever wondered how you should bet in craps during the point roll phase.",
                    "Rolling a 7 has the highest probability of of 16.66%,so the house always has the edge on you. Seems unfair doesn't it?",
                    "If you roll a 6 or 8 that has the highest probablity of 13.89%, so bet high",
                    "If you roll a 5 or 9 then going a medium kind of bet is best with a 11.11% probability.",
                    "A roll of 4 and 10 has a probablity of 8.33% so bet low",
                    "A roll of 3 and 11 has a probablity of 5.56% so bet  low if you roll an 11",
                    "A roll of 2 and 12 has a probablity of 2.78% ,though that wont matter much as you cant st that as point roll ",



                ],
                (50, 450, 50, 45), 30, 500
            ),
            "erika_in_party": NpcTextBox(
                [
                    "Nataliet: Have you had a chance to equip your companion item? It'll help a lot in winning craps",
                    "WIth a spirit of 2  you can equip it, but you knew that already didn't you? "

                ],
                (50, 450, 50, 45), 30, 500
            ),
        }
        self.choices = ["Yes", "No"]
        self.sprite_sheet = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/cindy_text_talk_image_2.png").convert_alpha()

        # The size of the entire sprite sheet
        self.sprite_sheet_width = self.sprite_sheet.get_width()
        self.sprite_sheet_height = self.sprite_sheet.get_height()

        # The size of an individual sprixxxxte
        self.sprite_width = self.sprite_sheet_width // 22
        self.sprite_height = self.sprite_sheet_height
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.coinFlipTedReward = False

        # self.character_sprite_image = pygame.image.load(
        #     "/Users/stevenhalla/code/casino_hell/assets/images/cindy_long_hair_sprites.png")

        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/snes-anna-hmllllllll.png").convert_alpha()

        # Set the color key for transparency (replace (0, 255, 0) with the exact RGB value of your light green)
        self.character_sprite_image.set_colorkey((120,195,128))

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

        # self.sprite_sheet = pygame.image.load("./assets/images/cindy_text_talk_image_2.png")

    def update(self, state: "GameState"):
        if self.state == "waiting":
            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":
            # Determine which message to use based on player state
            current_message = self.npc_messages["default_message"]
            if Events.ERIKA_IN_PARTY.value in state.player.companions:
                current_message = self.npc_messages["erika_in_party"]

            if current_message.message_index == 1:
                if state.controller.isAPressed and pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"


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

            if distance < 40 and state.player.menu_paused == False:
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                # Reset the message based on player state
                current_message = self.npc_messages["default_message"]
                if Events.ERIKA_IN_PARTY.value in state.player.companions:
                    current_message = self.npc_messages["erika_in_party"]

                current_message.reset()

    def update_talking(self, state: "GameState", current_message):
        current_message.update(state)
        state.player.canMove = False

        if state.controller.isTPressed and current_message.is_finished():
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            state.player.canMove = True


    def draw(self, state):

        sprite_rect = pygame.Rect(5, 6, 21, 25)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw the correct message box based on the state of the NPC
        if self.state == "talking":
            current_message = self.npc_messages["default_message"]
            if Events.ERIKA_IN_PARTY.value in state.player.companions:
                current_message = self.npc_messages["erika_in_party"]
            current_message.draw(state)



