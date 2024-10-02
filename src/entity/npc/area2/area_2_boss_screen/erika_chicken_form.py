

import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.events import Events


class ErikaChickenForm(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        # sir leopold : How are you a free range chicken?
        self.npc_messages = {
            "welcome_message": NpcTextBox(
                [
                    "Erika: You don't have to do this hero, fighting the boss I'm worried for you, can't we just go up to the 3rd level?.",
                    "Hero: Why are you so worried for Erika? I'm here to bankrupt the boss of this floor and make a deal. I can handle myself fine",
                    "Sir Leopold:Hero My nose is itchy, something is off, she's acting weird, more so than usual, be on your guard",
                    "Erika:That's a real shame, I'll go ahead and introduce you to the boss, close your eyes, no peeking.",
                    "Remember no peeking you perverts"
                ],
                (50, 450, 50, 45), 30, 500
            ),


        }

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)
        self.quest_accepted = False
        self.current_screen = "welcome"



        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/chicken_sprites.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        distance = math.sqrt((player.collision.x - self.collision.x) ** 2 +
                             (player.collision.y - self.collision.y) ** 2)

        if distance < 40 and state.controller.isTPressed and \
                (pygame.time.get_ticks() - self.state_start_time) > 500 and state.player.menu_paused == False:
            self.state = "talking"
            self.state_start_time = pygame.time.get_ticks()


            self.npc_messages["welcome_message"].reset()

    def update_talking(self, state: "GameState"):
        print(state.area2BossScreen.black_screen)

        current_message = (
            self.npc_messages["welcome_message"]
            if state.player.hasRabies
            else (
                self.npc_messages["welcome_message"]

            )
        )
        current_message.update(state)

        if self.npc_messages["welcome_message"].message_index == len(self.npc_messages["welcome_message"].messages) - 1:
            state.area2BossScreen.black_screen = True

        # Lock the player in place while talking
        state.player.canMove = False

        # Check for keypresses only once per frame



        # Check if the "T" key is pressed and the flag is not set
        if current_message.is_finished() and current_message.message_at_end() and state.controller.isTPressed:



            # Reset the flag when the "T" key is released
            if not state.controller.isTPressed:
                self.t_pressed = False

        if state.controller.isTPressed and current_message.is_finished():
            state.controller.isTPressed = False
            # Exiting the conversation
            self.state = "waiting"
            self.menu_index = 0
            self.arrow_index = 0
            self.state_start_time = pygame.time.get_ticks()

            # Unlock the player to allow movement
            state.player.canMove = True

    def draw(self, state):
        # Draw character sprite
        # Coordinates of the sprite right of the white chicken
        sprite_rect = pygame.Rect(335, 65, 30, 30)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (55, 55))

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw the correct message box based on the state of the NPC
        if self.state == "talking":
            current_message = (
                self.npc_messages["welcome_message"]
                if state.player.hasRabies
                else (
                    self.npc_messages["welcome_message"]

                )
            )

            current_message.draw(state)


