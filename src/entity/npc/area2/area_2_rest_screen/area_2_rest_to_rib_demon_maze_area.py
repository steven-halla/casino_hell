import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment


class Area2RestToRibDemonMazeArea(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.selected_item_index = 0
        self.flipping_ted_messages = {
            "welcome_message": NpcTextBox(
                ["You need a key`"],
                (50, 450, 700, 130), 36, 500),
            "defeated_message": NpcTextBox(
                ["You have no reason to come here."],
                (50, 450, 700, 130), 36, 500)
        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"
        self.flipping_ted_defeated = False
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.t_pressed = False


        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/Game Boy Advance - Breath of Fire - Doof.png").convert_alpha()

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            current_message = self.flipping_ted_messages["welcome_message"]
            if Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value in state.player.items:
                current_message = self.flipping_ted_messages["defeated_message"]

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

        if (state.controller.isTPressed or state.controller.isAPressedSwitch) and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt((player.collision.x - self.collision.x) ** 2 + (player.collision.y - self.collision.y) ** 2)

            if distance < 40 and state.player.menu_paused == False:
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                # Reset the message based on player state
                current_message = self.flipping_ted_messages["welcome_message"]
                if Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value in state.player.items:
                    current_message = self.flipping_ted_messages["defeated_message"]

                current_message.reset()

    def update_talking(self, state: "GameState", current_message):
        current_message.update(state)
        state.player.canMove = False
        if "rib demon key" in state.player.quest_items and Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value not in state.player.items:
            state.area_2_rest_area_to_rib_demon_maze_point = True

            state.currentScreen = state.area2RibDemonMazeScreen
            state.area2RibDemonMazeScreen.start(state)

        if (state.controller.isTPressed or state.controller.isAPressedSwitch) and current_message.is_finished():
            self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            state.player.canMove = True






    def draw(self, state):


        if self.state == "talking" and Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value in state.player.items:
            current_message = self.flipping_ted_messages["defeated_message"]

            current_message.draw(state)

        elif self.state == "talking" and "rib demon key" not in state.player.quest_items:
            current_message = self.flipping_ted_messages["welcome_message"]
            current_message.draw(state)


