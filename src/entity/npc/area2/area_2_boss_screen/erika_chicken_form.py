

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
                    "Erika: You don't have to do this hero, fighting the boss...I'm worried for you, can't we just go up to the 3rd level like right now?.",
                    # "Sir Leopold: Why is she so nervous for? I didn't think it was possible to make a chicken sweat.",
                    # "Hero: I have my own reasons for wanting to battle the boss, and besides, I want to make a deal.",
                    # "Erika: Very well, don't say I didn't try and stop you. Close your eyes and I'll bring her out.",
                    # "Sir Leopold: Close our eyes? Why is that even needed for? Just bring them out already.",
                    # "Erika:Stop arguing and just close your eyes you perverts. Ok good, keep them closed.",
                    # "Remember no peeking or I'll peck you to death.",
                    # "Give me another mintue... Brrrr its a litlte cold in here. Gotta get these tight clothes on.....annddddddddd there.",
                    "Whew ok that is finally over, everything seems to be in order. Ok you can go ahead and look now you two.",
                    ""
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

        if self.npc_messages["welcome_message"].message_index == 7:
            state.area2BossScreen.black_screen = True

        if self.npc_messages["welcome_message"].message_index == len(self.npc_messages["welcome_message"].messages) - 1:
            state.currentScreen = state.area2BossAfterRevealScreen
            state.area2BossAfterRevealScreen.start(state)
            state.player.canMove = True
            self.state = "waiting"




        # Lock the player in place while talking
        if self.state is "talking":
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


