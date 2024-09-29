import math
import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class Natalie(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.cindy_long_hair_messages = {
            'textbox': NpcTextBox(
                [
                    "Natalie:Hi there I'm Cindy, you should know,  Cheating Ted is a real bastard. Because of him my boyfriend is making beer.",

                ],
                (50, 450, 50, 45), 36, 500
            ),
            'reward_message': NpcTextBox(
                [
                    "",
                    "Natalie: Oh cool look at you, time for your reward (inn badge). I have something else for you too, I don't just be giving these out.",


                ],

                (50, 450, 50, 45), 36, 500
            ),
            'final_message': NpcTextBox(
                [
                    "",
                    "Natalie: Watching you take him down was so satisfying thank you.",

                ],
                (50, 450, 50, 45), 36, 500
            ),
            'rabies_message': NpcTextBox(
                [
                    "",
                    "Natalie That witch Sally took the doctor's blue flower, I just know it.",
                    "Why else was she snooping around her office? You can't trust those opossum girls."
                ],
                (50, 450, 50, 45), 36, 500
            ),
            'sir_leopold_message': NpcTextBox(
                [
                    "",
                    "Natalie I was so scared...you have a knack for defying the odds.",
                    "Hero: What can I say, I guess Lady Luck is on my side.",

                ],
                (50, 450, 50, 45), 36, 500
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

        state.player.canMove = False


        if state.player.rabiesImmunity == True:
            current_message = self.cindy_long_hair_messages["sir_leopold_message"]

        elif state.player.hasRabies == True:
            current_message = self.cindy_long_hair_messages['rabies_message']

        elif self.coinFlipTedReward == True or state.restScreen.inn_badge_recieved_tracker == True:
            current_message = self.cindy_long_hair_messages['final_message']
        elif state.coinFlipTedScreen.coinFlipTedDefeated:
            if "reveal" not in state.player.magicinventory:
                state.player.magicinventory.append("reveal")
                state.player.npc_items.append("inn badge")
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
            if "reveal" in state.player.magicinventory:
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





        if self.state == "talking":
            sprite_rect = pygame.Rect(0, 0, 136, 186)  # Top left section with width and height of 100 pixels

            if state.player.rabiesImmunity == True:
                current_message = self.cindy_long_hair_messages["sir_leopold_message"]

            elif state.player.hasRabies == True:
                current_message = self.cindy_long_hair_messages['rabies_message']
            elif self.coinFlipTedReward == True or state.restScreen.inn_badge_recieved_tracker == True:

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



