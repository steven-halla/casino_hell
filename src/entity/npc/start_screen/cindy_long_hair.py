import math
import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class CindyLongHair(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.cindy_long_hair_messages = {
            'textbox': NpcTextBox(
                [
                    "Cindy: Cheating Ted is such a bastard. Because of him my boyfriend is making beer.",
                    "The key to winning is to pay attention to patterns, which can change in the middle of playing",
                    "Try betting low, and get  a hang for the patterns before you go in for the kill."
                ],
                (50, 450, 50, 45), 30, 500
            ),
            'reward_message': NpcTextBox(
                [
                    "",
                    "Cindy: Oh kool look at you, time for your reward (inn badge). Oh, you want something else too, what a greedy man you are!.",
                    "Ok I know just what you want.....I'll give you this potion bottoms up!",
                    "low: 1-9, med 10=15, high 16-21",

                ],

                (50, 450, 50, 45), 30, 500
            ),
            'final_message': NpcTextBox(
                [
                    "",
                    "Cindy: Watching you take him down was so satisfying thank you.",
                    "Black Jack Technique Reveal: Get a good sense of what your opponent has.",
                    "low: 1-9, med 10=15, high 16-21",
                ],
                (50, 450, 50, 45), 30, 500
            ),
            'rabies_message': NpcTextBox(
                [
                    "",
                    "that bitch Sally took teh doctors blue flower, I just know it.",
                ],
                (50, 450, 50, 45), 30, 500
            ),
            'sir_leopold_message': NpcTextBox(
                [
                    "",
                    "I was so scared....you have a knack for defying the odds.....",
                ],
                (50, 450, 50, 45), 30, 500
            ),
        }
        self.choices = ["Yes", "No"]
        self.sprite_sheet = pygame.image.load("/Users/stevenhalla/code/casino_hell/assets/images/cindy_text_talk_image_2.png").convert_alpha()

        # The size of the entire sprite sheet
        self.sprite_sheet_width = self.sprite_sheet.get_width()
        self.sprite_sheet_height = self.sprite_sheet.get_height()

        # The size of an individual sprite
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

        self.sprite_sheet = pygame.image.load("./assets/images/cindy_text_talk_image_2.png")

        # self.character_image = pygame.image.load(
        #     "/Users/stevenhalla/code/nfeGame/images/player_walk_0.png")

    # def draw_npc_text(self, position: tuple[int, int], display: pygame.Surface):
    #     top_card_position = (self.card_width * 13, 0)
    #     sprite = self.sprite_sheet.subsurface(pygame.Rect(top_card_position, (self.card_width, self.card_height)))
    #     sprite.set_colorkey((0, 190, 0))
    #     display.blit(sprite, position)


    def update(self, state: "GameState"):

        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

    def update_waiting(self, state: "GameState"):

        player = state.player
        min_distance = math.sqrt(
            (player.collision.x - self.collision.x) ** 2 + (
                        player.collision.y - self.collision.y) ** 2)
        if min_distance < 10:
            print("nooo")

        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            if distance < 40:
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                self.cindy_long_hair_messages['textbox'].reset()



    def update_talking(self, state: "GameState"):
   # This will print the color of the pixel (R, G, B, A)

        # Don't forget to quit Pygame if you're done



        state.player.canMove = False


        if "sir leopold" in state.player.companions:
            current_message = self.cindy_long_hair_messages["sir_leopold_message"]

        elif state.player.hasRabies == True:
            current_message = self.cindy_long_hair_messages['rabies_message']

        elif self.coinFlipTedReward == True:
            current_message = self.cindy_long_hair_messages['final_message']
        elif state.coinFlipTedScreen.coinFlipTedDefeated:
            if "reveal" not in state.player.magicinventory:
                state.player.magicinventory.append("reveal")
                state.player.items.append("inn badge")
            if state.player.mind < 1:
                state.player.mind += 1

            current_message = self.cindy_long_hair_messages['reward_message']
        else:
            current_message = self.cindy_long_hair_messages['textbox']
        current_message.update(state)
        if state.controller.isTPressed and current_message.is_finished():
            self.state = "waiting"
            state.player.canMove = True

            self.state_start_time = pygame.time.get_ticks()
            current_message.reset()  # Ensure the message is reset for the next interaction
            if "black jack reveal" in state.player.magicinventory:
                self.coinFlipTedReward = True


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
        #
        # sprite_rect = pygame.Rect(5, 5, 22, 22)
        #
        # # Get the subsurface for the area you want
        # sprite = self.character_sprite_image.subsurface(sprite_rect)
        #
        # # Scale the subsurface to make it two times bigger
        # scaled_sprite = pygame.transform.scale(sprite, (88, 88))  # 44*2 = 88
        #
        # # Define the position where you want to draw the sprite
        # sprite_x = self.collision.x + state.camera.x
        # sprite_y = self.collision.y + state.camera.y - 10
        #
        # # Draw the scaled sprite portion on the display
        # state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # original_width, original_height = self.character_image.get_size()

        # # Calculate the new dimensions
        # new_width = original_width * 2
        # new_height = original_height * 2

        # Scale the image
        # scaled_image = pygame.transform.scale(self.character_sprite_image, (new_width, new_height))
        #
        # sprite_x = self.collision.x + state.camera.x
        # sprite_y = self.collision.y + state.camera.y - 10

        # state.DISPLAY.blit(scaled_image, (sprite_x, sprite_y))

        # original_width, original_height = self.character_sprite_image.get_size()
        #
        # # Calculate the new dimensions of the image
        # new_width = original_width * 1.7
        # new_height = original_height * 1.7
        #
        # # Scale the image
        # scaled_image = pygame.transform.scale(self.character_sprite_image,
        #                                       (new_width, new_height))
        # # Draw the scaled character sprite
        # state.DISPLAY.blit(scaled_image, (sprite_x, sprite_y))

        # rect = (
        #     self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        #     self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "talking":
            sprite_rect = pygame.Rect(0, 0, 136, 186)  # Top left section with width and height of 100 pixels

            # Extract the sprite section
            # sprite = self.sprite_sheet.subsurface(sprite_rect)

            # Center the sprite section on the screen
            # position_x = 60  # Bottom left corner x position
            # position_y = state.DISPLAY.get_height() - sprite_rect.height - 155  # 30 pixels above the bottom left corner y position
            # position = (position_x, position_y)
            #
            # # Draw the sprite section
            # state.DISPLAY.blit(sprite, position)

            if "sir leopold" in state.player.companions:
                current_message = self.cindy_long_hair_messages["sir_leopold_message"]

            elif state.player.hasRabies == True:
                current_message = self.cindy_long_hair_messages['rabies_message']
            elif self.coinFlipTedReward == True:
                current_message = self.cindy_long_hair_messages['final_message']
            elif state.coinFlipTedScreen.coinFlipTedDefeated:
                current_message = self.cindy_long_hair_messages['reward_message']
            else:
                current_message = self.cindy_long_hair_messages['textbox']
            current_message.draw(state)
            while state.coinFlipTedScreen.coinFlipTedDefeated == True and "black jack reveal" not in state.player.magicinventory:

                print(state.player.magicinventory)
                print(state.player.mind)
                # self.coinFlipTedReward = True

                return



