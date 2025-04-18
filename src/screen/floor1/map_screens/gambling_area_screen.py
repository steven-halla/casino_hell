import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.npc.battle_screen.Guy import Guy
from entity.npc.battle_screen.black_jack_thomas import BlackJackThomas
from entity.npc.battle_screen.coin_flip_fred import CoinFlipFred
from entity.npc.battle_screen.nelly_opossum import NellyOpossum
from entity.npc.battle_screen.rest_area_teleporter import RestScreenTeleporter
from entity.npc.chilli_screen.rumble_bill import RumbleBill
from entity.npc.battle_screen.sally_opossum import SallyOpossum
from entity.npc.hedge_maze_screen.hedgehog1 import HedgeHog1
from entity.npc.hedge_maze_screen.hedgehog2 import HedgeHog2
from entity.npc.hedge_maze_screen.hedgehog3 import HedgeHog3
from entity.npc.hedge_maze_screen.hedgehog4 import HedgeHog4
from entity.npc.inn_guard import InnGuard
from entity.npc.nurgle import Nurgle
from entity.player.player import Player
from screen.examples.screen import Screen
from physics.rectangle import Rectangle


class GamblingAreaScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/gamblingarea.tmx")
        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.player = Player(333, 555)
        self.hedge_hog_counter = 0
        move_player_down_flag = False
        self.five_hundred_opossums = False
        self.nurgle_the_hedge_hog = False
        self.npcs = []  # Initialize the NPCs list as empty
        self.music_file = "./assets/music/town_music.mp3"
        self.music_volume = 0.5  # Adjust as needed
        self.initialize_music()
        self.clock = pygame.time.Clock()  # Initialize the clock





    def stop_music(self):
        pygame.mixer.music.stop()

    def initialize_music(self):
        # Initialize the mixer
        pygame.mixer.init()

        # Load the music file
        pygame.mixer.music.load(self.music_file)

        # Set the volume for the music (0.0 to 1.0)
        pygame.mixer.music.set_volume(self.music_volume)

        # Play the music, -1 means the music will loop indefinitely
        pygame.mixer.music.play(-1)



    def start(self, state: "GameState"):
        self.stop_music()
        if state.musicOn == True:
            self.initialize_music()
        super().start(state)

        if state.rest_area_to_gambling_area_entry_point == True:
            player_start_x = 16 * 18  # Desired X coordinate
            player_start_y = 16 * 51  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.rest_area_to_gambling_area_entry_point = False




        state.npcs = []

        if self.nurgle_the_hedge_hog == True and state.restScreen.rest_screen_npc_janet_find_hog == False and state.player.perception > 0:
            print("Before appending Nurgle, NPCs:", state.npcs)
            state.npcs.append(Nurgle(16 * 25, 16 * 22))
            print("After appending Nurgle, NPCs:", state.npcs)

        #
        # if "Nurgle the hedge hog" in state.player.items:
        #     state.npcs.remove(Nurgle(16 * 25, 16 * 22))

        # state.npcs = []




        state.npcs.extend([
            BlackJackThomas(16 * 30, 16 * 22),
            CoinFlipFred(16 * 12, 16 * 28),
            NellyOpossum(16 * 30, 16 * 7),
            SallyOpossum(16 * 5, 16 * 5),
            Guy(16 * 42, 16 * 44),
            RestScreenTeleporter(16 * 19, 16 * 54),
        ])



    def update(self, state: "GameState"):


        self.clock.tick(60)
        if state.player.stamina_points < 1:
            state.player.money -= 100
            state.currentScreen = state.restScreen
            state.restScreen.start(state)
            state.player.stamina_points = 1
            if state.player.money < 1:
                state.currentScreen = state.gameOverScreen
                state.gameOverScreen.start(state)

        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()
        for npc in state.npcs:
            npc.update(state)
            if isinstance(npc, Nurgle) and npc.to_be_deleted:
                state.npcs.remove(npc)
                state.restScreen.rest_screen_npc_janet_find_hog = True




        ### i can use this to append NPC if i need to , just state.npcs.append(npc)
        # for npc in state.npcs:
        #     npc.update(state)
        #     # Check if the npc is any of the hedgehogs
        #     if isinstance(npc, (HedgeHog1, HedgeHog2, HedgeHog3, HedgeHog4)) and npc.to_be_deleted:
        #         self.hedge_hog_counter += 1
        #         print(self.hedge_hog_counter)
        #         state.npcs.remove(npc)

        # Game Update Loop
        for chest in state.treasurechests:
            chest.update(state)


        if controller.isExitPressed is True:
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

        for demon in state.demons:
            demon.draw(state)

        for treasurechests in state.treasurechests:
            treasurechests.draw(state)



        state.obstacle.draw(state)

        state.player.draw(state)

        if state.controller.isPPressed == True:

            state.player.draw_player_stats(state)

            if state.controller.isBPressed == True:
                if state.controller.isPPressed:
                    state.controller.isPPressed = False
                    return



        # Update the display
        pygame.display.update()
