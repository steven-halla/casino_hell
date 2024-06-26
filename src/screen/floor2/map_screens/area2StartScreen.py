import pygame
import pytmx
from pygame import display
from constants import PLAYER_OFFSET, BLUEBLACK, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, BLACK, WHITE
from entity.npc.hedge_maze_screen.hedgehog1 import HedgeHog1
from entity.npc.hedge_maze_screen.hedgehog2 import HedgeHog2
from entity.npc.hedge_maze_screen.hedgehog3 import HedgeHog3
from entity.npc.hedge_maze_screen.hedgehog4 import HedgeHog4
from entity.npc.start_screen.bapping_mike import BappingMike
from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.npc.start_screen.flippin_ted import FlippinTed
from entity.npc.start_screen.hungry_patrick import HungryPatrick
from entity.npc.jacky_banana import JackyBanana
from entity.npc.start_screen.main_screen_teleporter import MainScreenTeleporter
from entity.npc.nicky_hints import NickyHints
from entity.player.player import Player
from screen.examples.screen import Screen
from physics.rectangle import Rectangle


class Area2StartScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/startscreen1.tmx")
        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.hedge_hog_counter = 0
        move_player_down_flag = False
        self.lock_screen = False

        self.music_file = "/Users/stevenhalla/code/casino_hell/assets/music/town_music.mp3"
        self.music_volume = 0.5  # Adjust as needed
        self.initialize_music()

        self.clock = pygame.time.Clock()  # Initialize the clock

    def stop_music(self):
        pygame.mixer.music.stop()

    def initialize_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def start(self, state: "GameState"):
        self.stop_music()
        if state.musicOn:
            self.initialize_music()
        super().start(state)

        if state.start_new_game_entry_point:
            player_start_x = 16 * 33
            player_start_y = 16 * 26
            state.player.setPosition(player_start_x, player_start_y)
            state.start_new_game_entry_point = False
        elif state.rest_area_to_start_area_entry_point:
            player_start_x = 44 * 18.5
            player_start_y = 16 * 4
            state.player.setPosition(player_start_x, player_start_y)
            state.rest_area_to_start_area_entry_point = False

        state.npcs = []
        # print("NPCs after setting to empty list:", state.npcs)

    def update(self, state: "GameState"):
        state.npcs = []

        start_time = pygame.time.get_ticks()
        self.clock.tick(60)
        end_time = pygame.time.get_ticks()

        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()

        # print(f"NPCs state before update: {state.npcs}")

        if controller.isExitPressed:
            state.isRunning = False

        if controller.isUpPressed:
            self.y_up_move = True
            self.y_down_move = False
            self.x_left_move = False
            self.x_right_move = False
        elif controller.isDownPressed:
            self.y_down_move = True
            self.y_up_move = False
            self.x_left_move = False
            self.x_right_move = False
        elif controller.isLeftPressed:
            self.x_left_move = True
            self.y_up_move = False
            self.y_down_move = False
            self.x_right_move = False
        elif controller.isRightPressed:
            self.x_right_move = True
            self.y_up_move = False
            self.y_down_move = False
            self.x_left_move = False
        else:
            self.y_up_move = False
            self.y_down_move = False
            self.x_left_move = False
            self.x_right_move = False

        player.update(state)

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

        # print(f"NPCs state after update: {state.npcs}")

    def draw(self, state: "GameState"):
        state.DISPLAY.fill(BLUEBLACK)
        if self.tiled_map.layers:
            tile_width = self.tiled_map.tilewidth
            tile_height = self.tiled_map.tileheight
            bg_layer = self.tiled_map.get_layer_by_name("bg")
            for x, y, image in bg_layer.tiles():
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y
                scaled_image = pygame.transform.scale(image, (tile_width * 1.3, tile_height * 1.3))
                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))
            collision_layer = self.tiled_map.get_layer_by_name("collision")
            for x, y, image in collision_layer.tiles():
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y
                scaled_image = pygame.transform.scale(image, (tile_width * 1.3, tile_height * 1.3))
                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))

        for npc in state.npcs:
            npc.draw(state)
            # print(f"Drawing NPC: {npc}")

        state.player.draw(state)

        if state.controller.isPPressed:
            state.player.draw_player_stats(state)
            if state.controller.isBPressed:
                if state.controller.isPPressed:
                    state.controller.isPPressed = False
                    # print("Mew")
                    return

        pygame.display.update()
