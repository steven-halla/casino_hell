import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.events import Events


#### NOTE: BOTH JANET AND BILLY BOTH NEED HEDGE HOG AND WATER WILL NEED TO CHANGE IN FUTURE
####
####
class Jasper(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.npc_messages = {
            "default_message": NpcTextBox(
                [
                    "Jasper: If you increase your perception outside of gambling, be sure to leave the area and come back, or the treasure chest wont reveal themselves",
                    "Hero: why is that? That doens't make any sense?",
                    "Jasper: The treasure chest  are shy, they dont like to show themselves coming out of hiding.",
                    "Hero: Wait the treasure chest are alive??? ",
                    "Jasper: Well yeah of course they are, why do you think they vanish after you open them? "
                ],
                (50, 450, 50, 45), 30, 500
            ),
            "erika_in_party": NpcTextBox(
                [
                    "Jasper: I find the water to be relaxing and calming, it's the little things in life that are important.",


                ],
                (50, 450, 50, 45), 30, 500
            ),
        }


        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        self.textboxstate = "textbox1" # state = "textbox1" | "textbox2" | "textbox3" | "textbox4" | "textbox5"

        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/snes-anna-hmllllllll.png").convert_alpha()

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
        sprite_rect = pygame.Rect(212, 6, 18, 25)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        if state.restScreen.bar_keeper_talking == False:
            state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        if self.state == "talking":
            current_message = self.npc_messages["default_message"]
            if Events.ERIKA_IN_PARTY.value in state.player.companions:
                current_message = self.npc_messages["erika_in_party"]
            current_message.draw(state)

