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


class Area2BarCutScene1(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/casinomaingame4.tmx")

        self.player = Player(333, 555)
        move_player_down_flag = False
        self.npcs = []
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
        self.cut_scene_movement.move_right(state.player)

        elapsed_time = time.time() - self.timer_start  # Calculate elapsed time
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")

        # Check if elapsed time is greater than 2 seconds
        if elapsed_time >= 2:
            print("puffy")
            self.display_message1 = True

            # Open the text box
            current_message = self.cut_scene_1_messages["message_1"]
            current_message.update(state)

        current_time = time.time()

        # Example of stopping movement after 2 seconds (adjust event_timer as needed)
        event_timer = 2  # seconds
        self.cut_scene_movement.stop_movement(current_time, event_timer)

        # Increment the timer by the time elapsed since the last frame
        # Calculate the time elapsed since the screen started



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

        if self.display_message1:
            self.cut_scene_1_messages["message_1"].draw(state)

        state.obstacle.draw(state)

        state.player.draw(state)

        # Update the display
        pygame.display.update()
