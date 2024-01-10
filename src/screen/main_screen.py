import pygame
import pytmx

from entity.npc.bapping_mike import BappingMike
from entity.npc.bar_keep import BarKeep
from entity.npc.bobby_bibs import BobbyBibs
from entity.npc.brutal_patrick import BrutalPatrick
from entity.npc.chilly_billy import ChillyBilly
from entity.npc.cindy_long_hair import CindyLongHair
from constants import PLAYER_OFFSET, BLUEBLACK
from entity.npc.coin_flip_fred import CoinFlipFred
from entity.npc.flippin_ted import FlippinTed
from entity.npc.inn_guard import InnGuard
from entity.player.player import Player
from screen.screen import Screen
from entity.npc.jacky_banana import JackyBanana
from entity.npc.justin_no_fruit import JustinNoFruit
from entity.npc.nicky_hints import NickyHints
from physics.rectangle import Rectangle
from entity.npc.rumble_bill import RumbleBill
from entity.npc.sally_opossum import SallyOpossum
from entity.npc.sleepy_ned import SleepyNed
from entity.npc.wally_guide import WallyGuide


class MainScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        # Load the Tiled map file
        self.tiled_map = pytmx.load_pygame("./assets/map/casinomaingame4.tmx")

        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False

    def start(self, state: "GameState"):
        super().start(state)

        player_start_x = 100  # Replace these values with your desired starting position
        player_start_y = 200  # Replace these values with your desired starting position

        # Create an instance of Player with the specified starting position
        state.player = Player(player_start_x, player_start_y)
        # state.npcs = []
        state.npcs = [
            # make sure to seperate by a factor of 8 for y
            #x, y
            InnGuard(16 * 36, 16 * 2),
            BappingMike(16 * 36, 16 * 10),
            BarKeep(16 * 36, 16 * 18),
            BobbyBibs(16 * 2, 16 * 2),
            BrutalPatrick(16 * 2, 16 * 10),
            ChillyBilly(16 * 2, 16 * 18),
            CindyLongHair(16 * 2, 16 * 26),
            CoinFlipFred(16 * 2, 16 * 34),
            FlippinTed(16 * 20, 16 * 36),



                      ]

    def update(self, state: "GameState"):
        # i dont think npc and demons getting updated

        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()
        for npc in state.npcs:
            npc.update(state)

        if controller.isExitPressed is True:
            state.isRunning = False

        if state.player.inn_badge == True:
            for npc in state.npcs:
                if isinstance(npc, InnGuard):
                    state.npcs.remove(npc)

        # state.player.setPosition(state.player.position.x + state.player.velocity.x,
        #                          state.player.position.y + state.player.velocity.y)

        # obstacle.update(state)

        # When pressing two buttons at once, it will cause the button to stay true need to handle multiple button press

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

        # player.update(state)
        # the below if you set distace, the distance starts at the start point of game ,
        # if player moves, then distance variables will not work

        player.update(state)

        # check map for collision
        if self.tiled_map.layers:
            tile_rect = Rectangle(0, 0, 16, 16)
            collision_layer = self.tiled_map.get_layer_by_name("collision")
            # door_layer_rest = self.tiled_map.get_layer_by_name("door rest")
            # door_layer_boss = self.tiled_map.get_layer_by_name("door boss")
            # door_layer_hedge_hog_maze = self.tiled_map.get_layer_by_name("door hedge hog maze")
            for x, y, image in collision_layer.tiles():
                tile_rect.x = x * 16
                tile_rect.y = y * 16
                if state.player.collision.isOverlap(tile_rect):
                    state.player.undoLastMove()

            # for x,y, image in door_layer_rest.tiles():
            #     tile_rect.x = x * 16
            #     tile_rect.y = y * 16
            #     if state.player.collision.isOverlap(tile_rect):
            #         print("door map")
            #         state.currentScreen = state.restScreen
            #         state.restScreen.start(state)

            # for x,y, image in door_layer_boss.tiles():
            #     tile_rect.x = x * 16
            #     tile_rect.y = y * 16
            #     if state.player.collision.isOverlap(tile_rect):
            #         print("door map")
            #         state.currentScreen = state.bossScreen
            #         state.bossScreen.start(state)

            # for x,y, image in door_layer_hedge_hog_maze.tiles():
            #     tile_rect.x = x * 16
            #     tile_rect.y = y * 16
            #     if state.player.collision.isOverlap(tile_rect):
            #         print("door map")
            #         state.currentScreen = state.hedgeMazeScreen
            #         state.hedgeMazeScreen.start(state)

        state.camera.x = PLAYER_OFFSET[0] - state.player.collision.x
        state.camera.y = PLAYER_OFFSET[1] - state.player.collision.y

    def draw(self, state: "GameState"):
        state.DISPLAY.fill(BLUEBLACK)
        state.DISPLAY.blit(state.FONT.render(
            f"player money: {state.player.money}",
            True, (255, 255, 255)), (333, 333))
        state.DISPLAY.blit(state.FONT.render(
            f"player stamina points: {state.player.stamina_points}",
            True, (255, 255, 255)), (333, 388))

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

                # Blit the tile image to the screen at the correct position
                # state.DISPLAY.blit(image, (pos_x, pos_y))

            # objects_layer = self.tiled_map.get_layer_by_name("door rest")
            # for x, y, image in objects_layer.tiles():
            #     # Calculate the position of the tile in pixels
            #     pos_x = x * tile_width + state.camera.x
            #     pos_y = y * tile_height + state.camera.y
            #     scaled_image = pygame.transform.scale(image, (tile_width * 1.3, tile_height * 1.3))
            #
            #     tile_rect = Rectangle(pos_x, pos_y, tile_width, tile_height)
            #
            #     if state.player.collision.isOverlap(tile_rect):
            #         print("hi there")
            #         # state.currentScreen = state.restScreen
            #         # state.restScreen.start(state)
            #
            #     # Blit the tile image to the screen at the correct position
            #     state.DISPLAY.blit(scaled_image, (pos_x, pos_y))
        #
        for npc in state.npcs:
            npc.draw(state)

        state.obstacle.draw(state)

        state.player.draw(state)

        # Update the display
        pygame.display.update()
