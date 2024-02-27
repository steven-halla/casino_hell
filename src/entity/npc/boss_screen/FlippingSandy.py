import math
import pygame
from entity.gui.textbox.text_box import TextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

class FlippingSandy(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.selected_item_index = 0
        self.black_jack_thomas_messages = {
            "welcome_message": NpcTextBox(
                ["Buck: They make me drink beer till I'm almost ready to pop."],
                (50, 450, 700, 130), 36, 500),
            "defeated_message": NpcTextBox(
                ["Looks like you defeated me, how sad :("],
                (50, 450, 700, 130), 36, 500)
        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"
        self.sandy_defeated = False
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.t_pressed = False

        self.character_sprite_image = pygame.image.load(
             "/Users/stevenhalla/code/casino_hell/assets/images/horse.png").convert_alpha()

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
                (pygame.time.get_ticks() - self.state_start_time) > 500:
            self.state = "talking"
            self.state_start_time = pygame.time.get_ticks()
            # Reset the message depending on the game state
            if state.blackJackThomasScreen.black_jack_thomas_defeated:
                self.black_jack_thomas_messages["defeated_message"].reset()
            else:
                self.black_jack_thomas_messages["welcome_message"].reset()

    def update_talking(self, state: "GameState"):
        current_message = self.black_jack_thomas_messages["defeated_message"] if state.coinFlipSandyScreen.coinFlipSandyDefeated else self.black_jack_thomas_messages["welcome_message"]
        current_message.update(state)

        # Lock the player in place while talking
        state.player.canMove = False

        # Check for keypresses only once per frame
        if current_message.is_finished():

            if state.controller.isUpPressed:
                self.arrow_index = (self.arrow_index - 1) % len(self.choices)
                state.controller.isUpPressed = False

            elif state.controller.isDownPressed:
                self.arrow_index = (self.arrow_index + 1) % len(self.choices)
                state.controller.isDownPressed = False

        # Check if the "T" key is pressed and the flag is not set
        if current_message.is_finished() and state.controller.isTPressed:
            # Handle the selected option
            selected_option = self.choices[self.arrow_index]
            print(f"Selected option: {selected_option}")

            # Check if the selected option is "Yes" and execute the code you provided


            # Reset the flag when the "T" key is released
            if not state.controller.isTPressed:
                self.t_pressed = False

        if state.controller.isTPressed and current_message.is_finished() and state.coinFlipSandyScreen.coinFlipSandyDefeated == False:
            state.controller.isTPressed = False
            # Exiting the conversation
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()

            # Unlock the player to allow movement
            state.player.canMove = True

    def draw(self, state):
        # rect = (
        #     self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        #     self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)

        sprite_rect = pygame.Rect(1, 80, 31, 28)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (60, 60))
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        if self.state == "talking":
            current_message = self.black_jack_thomas_messages["defeated_message"] if state.coinFlipSandyScreen.coinFlipSandyDefeated else self.black_jack_thomas_messages["welcome_message"]
            current_message.draw(state)

            # Draw the "Yes/No" box only on the last message
