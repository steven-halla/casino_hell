

import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class BappingMike(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        self.guy_messages = {
            "default_message": NpcTextBox(
                [
                        "Mike: Money is FINITE, so don't waste it. You'll need it for gambling, sleeping, eating, as well as buying items.",
                        "Chinrog is the head demon of this level. He'll be gone in 10 days.",
                    "Hero: Demon? You know Demons aren't real right?",
                    "Mike: You didn't read the terms and conditions before signing it I bet.",
                    "Hero: Nope, it was 30 pages long, no thanks. Never had to fill one out at a casino before."
                ],
                (50, 450, 700, 130), 30, 500
            ),
            "rabies_message": NpcTextBox(
                ["You should go see a doctor, sadly for you I'm not a doctor.There is a doctor, very far away from me."],
                (50, 450, 700, 130), 36, 500
            ),
            "sir_leopold_message": NpcTextBox(
                ["How are you doing now? You'll need 2000 coins to get access to the boss area, from there you can go down to level 2. I believe in you."],
                (50, 450, 700, 130), 36, 500
            ),
        }

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()

        self.character_sprite_image = pygame.image.load(
             "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Carpenter.png").convert_alpha()
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"

    def update(self, state: "GameState"):
        if self.state == "waiting":
            player = state.player
            self.update_waiting(state)

        elif self.state == "talking":
            # Determine which message to use based on player state
            current_message = self.guy_messages["rabies_message"] if state.player.hasRabies else self.guy_messages["default_message"]

            if state.player.rabiesImmunity == True:
                current_message = self.guy_messages["sir_leopold_message"]

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
                if state.player.rabiesImmunity == True:
                    current_message = self.guy_messages["sir_leopold_message"]
                current_message.reset()

    def update_talking(self, state: "GameState", current_message):
        current_message.update(state)
        state.player.canMove = False
        if state.controller.isUpPressed:
            state.controller.isUpPressed = False
        if state.controller.isLeftPressed:
            state.controller.isLeftPressed = False

        if state.controller.isRightPressed:
            state.controller.isRightPressed = False

        if state.controller.isDownPressed:
            state.controller.isDownPressed = False

        if state.controller.isTPressed and current_message.is_finished():
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            state.player.canMove = True

    def draw(self, state):
        # Draw character sprite
        sprite_rect = pygame.Rect(5, 6, 18, 25)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # Draw the correct message box based on the state of the NPC
        if self.state == "talking":
            current_message = self.guy_messages["rabies_message"] if state.player.hasRabies else self.guy_messages["default_message"]
            if state.player.rabiesImmunity == True:
                current_message = self.guy_messages["sir_leopold_message"]
            current_message.draw(state)

