

import math
import pygame


from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.events import Events
from game_constants.magic import Magic


# in order to get this quest to work:
# if you win 500 coins get a coin
# if you win 500 coins from two games those coins become mega coin.
# if you rest at the innn, the lower coins vanish , but an inn stay wont eras the mega coin
class BrosephTalk(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        self.selected_item_index = 0
        self.cody_talk_messages = {
            "welcome_message": NpcTextBox(
                ["Broseph: I hate cake."],
                (50, 450, 700, 130), 36, 500),
            "quest_complete_message": NpcTextBox(
                ["Broseph: Hope the perception boost."],
                (50, 450, 700, 130), 36, 500),



        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"
        self.black_jack_thomas_defeated = False
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.t_pressed = False


        self.character_sprite_image = pygame.image.load(
            "./assets/images/SNES - Harvest Moon - Shipping Workers.png").convert_alpha()

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        distance = math.sqrt((player.collision.x - self.collision.x) ** 2 +
                             (player.collision.y - self.collision.y) ** 2)

        if (distance < 40 and state.controller.confirm_button and \
                (pygame.time.get_ticks() - self.state_start_time) > 500
                and state.player.menu_paused == False):
            self.state = "talking"
            self.state_start_time = pygame.time.get_ticks()



            self.cody_talk_messages["welcome_message"].reset()

    def update_talking(self, state: "GameState"):

        current_message = self.cody_talk_messages["welcome_message"]
        current_message.update(state)

        # Lock the player in place while talking
        state.player.canMove = False
        if state.player.money > 2000:
            state.player.perception = 1
            print("Here is your pereception booster")
        else:
            print("no")


        # Check for keypresses only once per frame
        if current_message.is_finished() and current_message.message_at_end():

            if state.controller.up_button:
                self.arrow_index = (self.arrow_index - 1) % len(self.choices)



            elif state.controller.down_button:
                self.arrow_index = (self.arrow_index + 1) % len(self.choices)


        if state.controller.confirm_button and current_message.is_finished():

            # Exiting the conversation
            self.state = "waiting"
            self.menu_index = 0
            self.arrow_index = 0
            self.state_start_time = pygame.time.get_ticks()

            # Unlock the player to allow movement
            state.player.canMove = True

    def draw(self, state, only_dialog=False):
        if not only_dialog:
            # Draw the NPC sprite
            sprite_rect = pygame.Rect(7, 6, 16.4, 24)
            sprite = self.character_sprite_image.subsurface(sprite_rect)
            scaled_sprite = pygame.transform.scale(sprite, (50, 50))
            sprite_x = self.collision.x + state.camera.x - 20
            sprite_y = self.collision.y + state.camera.y - 10
            state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Always draw dialog if talking
        if self.state == "talking":

            current_message = self.cody_talk_messages["welcome_message"]
            current_message.draw(state)
