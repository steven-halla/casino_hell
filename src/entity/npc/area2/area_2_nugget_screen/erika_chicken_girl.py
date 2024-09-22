

import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.events import Events


class ErikaChickenGirl(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        # sir leopold : How are you a free range chicken?
        self.npc_messages = {
            "default_message": NpcTextBox(
                [
                    "Erika: Hello Hero, would you like some animal parade chicken nuggies",
                    "Hero: No thank you I thinik I'm good on that",
                    "Erika: I need 3000 COINS to start my quest, I can give you the best item on this floor."
                ],
                (50, 450, 50, 45), 30, 500
            ),
            "quest_message": NpcTextBox(
                [
                    "Erika: I have a very special quest for you, can you pay me 2000 coins?(You need to be holding"
                    "3000 coins)",
               \

                ],
                (50, 450, 50, 45), 30, 500
            ),

        }

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)



        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Parents.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):
        if self.state == "waiting":
            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":
            # Determine which message to use based on player state

            if state.player.money >= 3000:
                current_message = self.npc_messages["quest_message"]
            else:
                current_message = self.npc_messages["default_message"]

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
                if state.player.money >= 3000:
                    current_message = self.npc_messages["quest_message"]
                else:
                    current_message = self.npc_messages["default_message"]

                current_message.reset()

    def update_talking(self, state: "GameState", current_message):
        current_message.update(state)
        state.player.canMove = False

        if state.controller.isTPressed and current_message.is_finished():
            if state.player.money >= 3000:
                state.player.money -= 2000

                state.player.level_two_npc_state.append(Events.CHICKEN_QUEST_START.value)

            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            state.player.canMove = True

    def yes_no_text_box(self, state):
        # Use the exact box dimensions, positions, and variables as specified
        bet_box_width = 150
        bet_box_height = 100
        border_width = 5

        screen_width, screen_height = state.DISPLAY.get_size()
        bet_box_x = screen_width - bet_box_width - border_width - 48
        bet_box_y = screen_height - 130 - bet_box_height - border_width - 60

        # Create the black box for Yes/No
        bet_box = pygame.Surface((bet_box_width, bet_box_height))
        bet_box.fill((0, 0, 0))

        # Create a white border for the black box
        white_border = pygame.Surface((bet_box_width + 2 * border_width, bet_box_height + 2 * border_width))
        white_border.fill((255, 255, 255))
        white_border.blit(bet_box, (border_width, border_width))

        # Draw the white-bordered box
        state.DISPLAY.blit(white_border, (bet_box_x, bet_box_y))

        # Calculate text positions
        text_x = bet_box_x + 50 + border_width
        text_y_yes = bet_box_y + 20
        text_y_no = text_y_yes + 40

        # Draw the text on the screen (over the box)
        state.DISPLAY.blit(self.font.render("Yes", True, (255, 255, 255)), (text_x, text_y_yes))
        state.DISPLAY.blit(self.font.render("No", True, (255, 255, 255)), (text_x, text_y_no))

        # Arrow position logic based on self.menu_index
        arrow_x = text_x - 30  # Adjust the position of the arrow based on your preference
        arrow_y = text_y_yes + self.menu_index * 40  # Adjust based on the current menu index

        # Draw the arrow next to the Yes/No options
        pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                            [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])


    def draw(self, state):
        # Draw character sprite

        sprite_rect = pygame.Rect(147, 6, 16, 28)

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
            if state.player.money >= 3000:
                self.yes_no_text_box(state)
                current_message = self.npc_messages["quest_message"]
            else:
                current_message = self.npc_messages["default_message"]

            current_message.draw(state)

