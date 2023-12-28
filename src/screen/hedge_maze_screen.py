import pygame

from entity.npc.bobby_bibs import BobbyBibs
from entity.npc.chilly_billy import ChillyBilly
from constants import PLAYER_OFFSET, BLUEBLACK
from screen.screen import Screen
from entity.npc.hungry_patrick import HungryPatrick
from physics.rectangle import Rectangle
from entity.npc.suffering_suzy import SufferingSuzy


class HedgeMazeScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        # Load the Tiled map file
        # self.tiled_map = pytmx.load_pygame("/Users/steven/code/games/casino/casino_sprites/chili_hedge_maze_beta.tmx")

        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False

    def start(self, state: "GameState"):
        super().start(state)
        state.npcs = []
        state.npcs = [ChillyBilly(16 * 3, 16 * 2),
                      SufferingSuzy(16 * 15, 16 * 2),
                      BobbyBibs(16 * 3, 16 * 12),
                      HungryPatrick(16 * 15, 16 * 12)]

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
            door_layer_main = self.tiled_map.get_layer_by_name("door main")

            for x, y, image in collision_layer.tiles():
                tile_rect.x = x * 16
                tile_rect.y = y * 16
                if state.player.collision.isOverlap(tile_rect):
                    state.player.undoLastMove()

            for x, y, image in door_layer_main.tiles():
                tile_rect.x = x * 16
                tile_rect.y = y * 16
                if state.player.collision.isOverlap(tile_rect):
                    print("door map")
                    state.currentScreen = state.mainScreen
                    state.mainScreen.start(state)

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

            objects_layer = self.tiled_map.get_layer_by_name("door main")
            for x, y, image in objects_layer.tiles():
                # Calculate the position of the tile in pixels
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y
                scaled_image = pygame.transform.scale(image, (
                tile_width * 1.3, tile_height * 1.3))

                tile_rect = Rectangle(pos_x, pos_y, tile_width, tile_height)

                if state.player.collision.isOverlap(tile_rect):
                    print("hi there")
                    # state.currentScreen = state.restScreen
                    # state.restScreen.start(state)

                # Blit the tile image to the screen at the correct position
                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))
        #
        for npc in state.npcs:
            npc.draw(state)

        state.obstacle.draw(state)

        state.player.draw(state)

        # Update the display
        pygame.display.update()
