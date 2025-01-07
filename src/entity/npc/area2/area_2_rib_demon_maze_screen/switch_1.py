import math
import pygame
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class Switch1(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.selected_item_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"
        self.font = pygame.font.Font(None, 36)
        self.t_pressed = False

        self.rect_height = 50
        self.rect_width = 25
        self.switch_color_off = (255, 0, 0)  # Red for off
        self.switch_color_on = (0, 255, 0)  # Green for on

        self.switch_activated = False  # Track if the switch is activated (permanently on)

        self.buy_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/BFBuyingSelling.wav")  # Adjust the path as needed
        self.buy_sound.set_volume(0.3)

        self.cant_buy_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/cantbuy3.wav")  # Adjust the path as needed
        self.cant_buy_sound.set_volume(0.5)

    def update(self, state: "GameState"):

        if state.area2RibDemonMazeScreen2.switch_1 == False:
            self.switch_activated = False
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        distance = math.sqrt((player.collision.x - self.collision.x) ** 2 +
                             (player.collision.y - self.collision.y) ** 2)

        # If the player is near the switch and presses 'T' and the switch is not yet activated
        if distance < 40 and (state.controller.isTPressed or state.controller.isAPressedSwitch) and not self.switch_activated and \
                (pygame.time.get_ticks() - self.state_start_time) > 500 and not state.player.menu_paused:

            self.state_start_time = pygame.time.get_ticks()

            # Activate the switch permanently
            if state.area2RibDemonMazeScreen2.switch_2 == False and \
                state.area2RibDemonMazeScreen2.switch_3 == False and \
                state.area2RibDemonMazeScreen2.switch_4 == False and \
                state.area2RibDemonMazeScreen2.switch_5 == False:
                    self.switch_activated = True
                    self.buy_sound.play()  # Play the sound effect once


                    state.area2RibDemonMazeScreen2.switch_1 = True
            else:
                self.switch_activated = False
                state.area2RibDemonMazeScreen2.switch_1 = False
                state.area2RibDemonMazeScreen2.switch_2 = False
                state.area2RibDemonMazeScreen2.switch_3 = False
                state.area2RibDemonMazeScreen2.switch_4 = False
                state.area2RibDemonMazeScreen2.switch_5 = False



            print("Switch 1 activated!")
            # state.area2RibDemonMazeScreen2.switch_1 = True
            # You can trigger any other logic related to the switch being activated here

    def update_talking(self, state: "GameState"):
        # Example talking state handling if needed
        pass

    def draw(self, state):
        # Determine the switch color based on its current state (on/off)
        switch_color = self.switch_color_on if self.switch_activated else self.switch_color_off

        # Draw the switch as a rectangle
        switch_rect = pygame.Rect(self.collision.x + state.camera.x,
                                  self.collision.y + state.camera.y,
                                  self.rect_width, self.rect_height)

        pygame.draw.rect(state.DISPLAY, switch_color, switch_rect)
