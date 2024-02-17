import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.demon.demon1 import Demon1
from entity.demon.demon2 import Demon2
from entity.demon.demon3 import Demon3
from entity.demon.demon4 import Demon4
from entity.npc.hedge_maze_screen.hedgehog1 import HedgeHog1
from entity.npc.hedge_maze_screen.hedgehog2 import HedgeHog2
from entity.npc.hedge_maze_screen.hedgehog3 import HedgeHog3
from entity.npc.hedge_maze_screen.hedgehog4 import HedgeHog4
from entity.npc.inn_guard import InnGuard
from entity.npc.nurgle import Nurgle
from entity.player.player import Player
from entity.treasurechests.blueflower import BlueFlower
from screen.examples.screen import Screen
from physics.rectangle import Rectangle


class HedgeMazeScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/hedgemaze1.tmx")
        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.player = Player(333, 555)
        self.hedge_hog_counter = 0
        self.blue_flower = False
        move_player_down_flag = False



    def start(self, state: "GameState"):
        super().start(state)

        # Check if a player instance already exists
        if not hasattr(state, 'player') or state.player is None:
            player_start_x = 300
            player_start_y = 200
            state.player = Player(player_start_x, player_start_y)

        state.treasurechests = [

            BlueFlower(16 * 7, 14 * 42),

        ]

        # state.npcs = []
        state.npcs = [

            HedgeHog1(16 * 43, 14 * 100),
            HedgeHog2(16 * 63, 14 * 118),
            HedgeHog3(16 * 52, 14 * 154),
            # HedgeHog4(16 * 53, 14 * 180), #THIS POSITION IS SET TO 1ST ENEMY
            # HedgeHog4(16 * 23, 14 * 198), # THIS POSITION IS BOTTOM LEFT CORNER OF SCREEN
            # HedgeHog4(16 * 2, 14 * 10),

            ]

        state.demons = [
            Demon1(16 * 53, 14 * 180),
            Demon1(16 * 20, 14 * 19),
            # Demon2(16 * 20, 14 * 79),
            # Demon3(16 * 20, 14 * 85),
            # Demon4(16 * 20, 14 * 10),
            # Demon3(16 * 20, 14 * 76),
            # Demon2(16 * 55, 16 * 13),
            # Demon3(16 * 55, 16 * 23),
            # Demon4(16 * 55, 16 * 33),
        ]

    def update(self, state: "GameState"):
        # i dont think npc and demons getting updated
        # print(state.quest_giver_janet.find_hog)
        # print(state.quest_giver_janet.quest2counter)
        if "blue flower" in state.player.items:
            state.currentScreen = state.chilliScreen
            state.chilliScreen.start(state)

        controller = state.controller
        # ... (rest of your update code) ...

        # Check if 'A' key is pressed
        if controller.isAPressed:
            # Instantiate Demon4 at a specific position (x, y)
            new_demon = Demon4(16 * 20, 16 * 10)  # You can set the position as needed
            # Add the new demon to the state.demons list
            state.demons.append(new_demon)


        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()
        for npc in state.npcs:
            npc.update(state)
            if isinstance(npc, Nurgle) and npc.to_be_deleted:
                state.npcs.remove(npc)

        # Assuming you have your hedgehog instances named like HedgeHog1, HedgeHog2, etc.
        # hedgehogs = [HedgeHog1(), HedgeHog2(), HedgeHog3(), HedgeHog4()]


        ### i can use this to append NPC if i need to , just state.npcs.append(npc)
        for npc in state.npcs:
            npc.update(state)
            # Check if the npc is any of the hedgehogs
            if isinstance(npc, (HedgeHog1, HedgeHog2, HedgeHog3, HedgeHog4)) and npc.to_be_deleted:
                self.hedge_hog_counter += 1
                print(self.hedge_hog_counter)
                state.npcs.remove(npc)

        # Game Update Loop
        for chest in state.treasurechests:
            chest.update(state)

        for demon in state.demons:
            demon.update(state)
            if demon.move_player_down:
                state.player.collision.y += 100  # Move player down by 100 pixels
                demon.move_player_down = False

        if controller.isExitPressed is True:
            state.isRunning = False

        if state.player.inn_badge == True:
            for npc in state.npcs:
                if isinstance(npc, InnGuard):
                    state.npcs.remove(npc)




        #
        # if state.coinFlipTedScreen.coinFlipTedDefeated == True and state.cindy_long_hair.coinFlipTedReward == True:
        #     coinMonicle = "coin monicle"
        #     state.player.items.append(coinMonicle)

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

    # def draw(self, state: "GameState"):
    #     state.DISPLAY.fill(BLUEBLACK)
    #     state.DISPLAY.blit(state.FONT.render(
    #         f"player money: {state.player.money}",
    #         True, (255, 255, 255)), (333, 333))
    #     state.DISPLAY.blit(state.FONT.render(
    #         f"player stamina points: {state.player.stamina_points}",
    #         True, (255, 255, 255)), (333, 388))
    #
    #     if self.tiled_map.layers:
    #         tile_width = self.tiled_map.tilewidth
    #         tile_height = self.tiled_map.tileheight
    #
    #         # Get the background layer
    #         bg_layer = self.tiled_map.get_layer_by_name("bg")
    #         # Iterate over the tiles in the background layer
    #         for x, y, image in bg_layer.tiles():
    #             # Calculate the position of the tile in pixels
    #             pos_x = x * tile_width + state.camera.x
    #             pos_y = y * tile_height + state.camera.y
    #
    #             scaled_image = pygame.transform.scale(image, (
    #                 tile_width * 1.3, tile_height * 1.3))
    #
    #             state.DISPLAY.blit(scaled_image, (pos_x, pos_y))
    #
    #         # Get the collision layer
    #         collision_layer = self.tiled_map.get_layer_by_name("collision")
    #         for x, y, image in collision_layer.tiles():
    #             # Calculate the position of the tile in pixels
    #             pos_x = x * tile_width + state.camera.x
    #             pos_y = y * tile_height + state.camera.y
    #
    #             scaled_image = pygame.transform.scale(image, (
    #                 tile_width * 1.3, tile_height * 1.3))
    #
    #             state.DISPLAY.blit(scaled_image, (pos_x, pos_y))
    #
    #     for npc in state.npcs:
    #         npc.draw(state)
    #         if isinstance(npc, WallyGuide):
    #             # Assuming npc.collision has x, y, width, and height attributes
    #             rect = (npc.collision.x, npc.collision.y, npc.collision.width, npc.collision.height)
    #             pygame.draw.rect(state.DISPLAY, (0, 255, 0), rect, 2)
    #
    #     for demon in state.demons:
    #         demon.draw(state)
    #
    #     for treasurechests in state.treasurechests:
    #         treasurechests.draw(state)
    #
    #     state.obstacle.draw(state)
    #
    #     state.player.draw(state)
    #
    #     # Draw Player's collision box in red
    #     pygame.draw.rect(state.DISPLAY, (255, 0, 0), state.player.collision.toTuple(), 2)
    #
    #     # ... (rest of your drawing code, like updating the display) ...
    #     pygame.display.update()

    def draw(self, state: "GameState"):
        state.DISPLAY.fill(BLUEBLACK)
        # state.DISPLAY.blit(state.FONT.render(
        #     f"player money: {state.player.money}",
        #     True, (255, 255, 255)), (333, 333))
        # state.DISPLAY.blit(state.FONT.render(
        #     f"player stamina points: {state.player.stamina_points}",
        #     True, (255, 255, 255)), (333, 388))

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

        # for npc in state.npcs:
        #     if isinstance(npc, ShopKeeper):
        #         npc.textbox.draw(state)

        for demon in state.demons:
            demon.draw(state)

        for treasurechests in state.treasurechests:
            treasurechests.draw(state)

        state.obstacle.draw(state)

        state.player.draw(state)

        # Update the display
        pygame.display.update()
