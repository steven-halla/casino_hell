import pygame
import pytmx
import time  # Import the time module

from constants import PLAYER_OFFSET, BLUEBLACK
from cut_scene_manager.cut_scene_movement import CutSceneMovement
from entity.gui.textbox.npc_text_box import NpcTextBox
from entity.npc.battle_screen.Guy import Guy

from entity.npc.chilli_screen.sir_leopold_the_hedgehog import SirLeopoldTheHedgeHog

from entity.npc.rest_screen.bar_keep import BarKeep

from entity.npc.rest_screen.quest_giver_janet import QuestGiverJanet

from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.player.player import Player
from screen.examples.screen import Screen
from physics.rectangle import Rectangle
from concurrent.futures import ThreadPoolExecutor



class Area2BarCutScene1(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/casinomaingame4.tmx")

        self.player = Player(333, 555)
        move_player_down_flag = False
        self.npcs = []

        self.timer_paused = False
        self.fixed_time = None
        self.initial_player_y = None

        self.cut_scene_movement = CutSceneMovement()
        self.timer_start = time.time()  # Initialize the timer at the start of the screen

        self.timer = 0  # Timer to track time since the screen started
        self.player_moved = False  # Flag to track if the player has been moved
        self.move_distance = 30  # Distance to move the player during the cutscene
        # Initialize the clock

        self.music_file =  "/Users/stevenhalla/code/casino_hell/assets/music/relax_screen.mp3"

        self.display_message1 = False  # Flag to track if the message should be displayed
        self.display_message2 = False  # Flag to track if the message should be displayed
        self.timer_start = None  # To store the start time of the timer
        self.timer_duration = 2


        self.cut_scene_1_messages = {
            "message_1": NpcTextBox(
                [
                    "Hero: So what is it going to take,to get some rule changes around here?",
                    "Hero: So what is it going to tak to get some stiches down here ?",




                ],
                (50, 450, 50, 45), 30, 500
            ),
            "message_2": NpcTextBox(
                ["Bro, you look totally sick, go see the doctor ASAP"],
                (50, 450, 700, 130), 36, 500
            ),
            "message_3": NpcTextBox(
                ["bro you look sic go see...oh wait your not longer sic never mind"],
                (50, 450, 700, 130), 36, 500
            ),
        }

        self.current_movement_index = 0
        self.movement_sequence = [
            ('move_right', 1),
            ('move_up', 1)
        ]
        self.event_counter = 0

        self.game_state = "step_1"
        self.state_start_time = None
        self.state_duration = 1  # Duration for each state

    def start(self, state: "GameState"):
        state.restScreen.barscene1 = True
        state.restScreen.bar_keeper_talking = False

        super().start(state)

        # self.timer_start = time.time()  # Initialize the timer at the start of the screen

        self.timer_start = time.time()  # Initialize the timer at the start of the screen

        # Check if a player instance already exists
        # times 16
        player_start_x = 300
        player_start_y = 300
        state.player = Player(player_start_x, player_start_y)

        state.npcs = []

    def update(self, state: "GameState"):

        current_time = time.time()

        if self.game_state == "step_1":
            if self.state_start_time is None:
                self.state_start_time = current_time
                self.state_duration = 1  # Set the duration for step_1

            elapsed_time = current_time - self.state_start_time
            print(f"STEP 1: Elapsed Time: {elapsed_time:.2f} seconds")

            if elapsed_time < self.state_duration:
                self.cut_scene_movement.move_right(state.player, duration=1)  # Trigger movement
            else:
                print("Timer set for STEP 1")
                self.cut_scene_movement.reset_movement()  # Reset the movement flag
                self.game_state = "step_2"  # Move to the next step
                self.state_start_time = None  # Reset timer for the next step

        elif self.game_state == "step_2":
            if self.state_start_time is None:
                self.state_start_time = current_time
                self.state_duration = 1  # Set the duration for step_2

            elapsed_time = current_time - self.state_start_time
            print(f"STEP 2: Elapsed Time: {elapsed_time:.2f} seconds")

            if elapsed_time < self.state_duration:
                self.cut_scene_movement.move_up(state.player, duration=1)  # Trigger movement
            else:
                print("Timer set for STEP 2")
                self.cut_scene_movement.reset_movement()  # Reset the movement flag
                self.game_state = "step_3"  # Move to the next step
                self.state_start_time = None  # Reset timer for the next step

        elif self.game_state == "step_3":

            print(f"STEP 3")

            self.current_message = self.cut_scene_1_messages["message_1"]
            self.current_message.update(state)
            if self.current_message.is_finished() and state.controller.isTPressed:
                print("hi")
                self.game_state = "step_4"
                state.controller.isTPressed = False


        # state.player.canMove = False
        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()

        if controller.isExitPressed is True:
            state.isRunning = False

        player.update(state)

        # check map for collision
        if self.tiled_map.layers:
            tile_rect = Rectangle(0, 0, 16, 16)
            collision_layer = self.tiled_map.get_layer_by_name("collision")

            for x, y, image in collision_layer.tiles():
                tile_rect.x = x * 16
                tile_rect.y = y * 16
                if state.player.collision.isOverlap(tile_rect):
                    state.player.undoLastMove()
                for demon in state.demons:
                    if demon.collision.isOverlap(tile_rect):
                        demon.undoLastMove()

        state.camera.x = PLAYER_OFFSET[0] - state.player.collision.x
        state.camera.y = PLAYER_OFFSET[1] - state.player.collision.y

    def draw(self, state: "GameState"):
        state.DISPLAY.fill(BLUEBLACK)

        if self.tiled_map.layers:
            tile_width = self.tiled_map.tilewidth
            tile_height = self.tiled_map.tileheight

            # Get the background layer
            bg_layer = self.tiled_map.get_layer_by_name("bg")
            # Iterate over the tiles in the background layer
            for x, y, image in bg_layer.tiles():
                # Calculate the position of the tile in pixels
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y

                scaled_image = pygame.transform.scale(image, (
                    tile_width * 1.3, tile_height * 1.3))

                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))

            # Get the collision layer
            collision_layer = self.tiled_map.get_layer_by_name("collision")
            for x, y, image in collision_layer.tiles():
                # Calculate the position of the tile in pixels
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y

                scaled_image = pygame.transform.scale(image, (
                    tile_width * 1.3, tile_height * 1.3))

                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))

        for npc in state.npcs:
            npc.draw(state)

        if self.game_state == "step_3":
            self.cut_scene_1_messages["message_1"].draw(state)

        state.obstacle.draw(state)

        state.player.draw(state)

        # Update the display
        pygame.display.update()