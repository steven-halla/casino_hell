import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.npc.area2trash.area_2_gambling_screen.area_2_gambling_to_rest_area import Area2GamblingToRestArea
from entity.npc.area2trash.area_2_gambling_screen.black_jack_mack import BlackJackMack
from entity.npc.area2trash.area_2_gambling_screen.coin_flip_betty import CoinFlipBetty
from entity.npc.area2trash.area_2_gambling_screen.happy_craps import CrapsHappy
from entity.npc.area2trash.area_2_gambling_screen.lunky import Lunky
from entity.npc.area2trash.area_2_gambling_screen.nibblet import Nibblet
from entity.npc.area2trash.area_2_gambling_screen.slots_rippa_snappa import SlotsRippaSnappa
from entity.npc.area2trash.area_2_gambling_screen.opossum_in_a_can_candy import OpossumInACanCandy
from entity.npc.area2trash.area_2_nugget_screen.area_2_nugget_to_rest_area import Area2NuggetToRestArea
from entity.npc.area2trash.area_2_nugget_screen.erika_chicken_girl import ErikaChickenGirl
from entity.npc.area2trash.area_2_nugget_screen.mcnugget import MCNugg

from entity.player.player import Player
from entity.treasurechests.slots_vest import SlotsVest
from game_constants.events import Events
from game_constants.treasure import Treasure
from screen.examples.screen import Screen
from physics.rectangle import Rectangle
from screen.floor2.map_screens.area_2_gambling_screen import Area2GamblingScreen
from screen.floor2.map_screens.area_2_rest_screen import Area2RestScreen


class Area2NuggetScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.chili_pit_flag = False
        self.tiled_map = pytmx.load_pygame("./assets/map/chilli.tmx")
        self.y_up_move = False
        self.powerpotiongotten = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.player = Player(333, 555)
        self.hedge_hog_counter = 0
        move_player_down_flag = False
        self.npcs = []  # Initialize the NPCs list as empty



        self.clock = pygame.time.Clock()  # Initialize the clock



        # self.music_file =  "./assets/music/relax_screen.mp3"
        #
        # self.music_volume = 0.5  # Adjust as needed
        # self.initialize_music()





    def start(self, state: "GameState"):


        if state.area_2_rest_area_to_nugget_point == True:
            print("nuggggggggggggggg;f")
            player_start_x = 16 * 35  # Desired X coordinate
            player_start_y = 16 * 32 # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.area_2_rest_area_to_nugget_point = False




        # self.stop_music()
        # if state.musicOn == True:
        #     self.initialize_music()
        super().start(state)
        state.npcs.clear()

        # Check if a player instance already exists
        # if not hasattr(state, 'player') or state.player is None:
        #     player_start_x = 300
        #     player_start_y = 200
        #     state.player = Player(player_start_x, player_start_y)



        if (Events.SLOTS_VEST_FOUND.value not in state.player.level_two_npc_state
                and state.player.perception > 2):
            state.treasurechests = [
                SlotsVest(16 * 5, 16 * 5),

            ]

        # Check the value of state.player.body

        # If the CHICKEN_QUEST_START event is not in level_two_npc_state, populate state.npcs

        state.npcs = [
            MCNugg(16 * 7, 16 * 17),
            ErikaChickenGirl(16 * 25, 16 * 3),
            Area2NuggetToRestArea(16 * 35, 16 * 34),
        ]

        print(str(state.player.level_two_npc_state))



    def update(self, state: "GameState"):


        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()


        #the below speeds up text speech
        # for npc in state.npcs:
        #     npc.update(state)
        #     if isinstance(npc, Nurgle) and npc.to_be_deleted:
        #         state.npcs.remove(npc)

        for npc in state.npcs:
            npc.update(state)
            if Events.CHICKEN_QUEST_START.value in state.player.level_two_npc_state:
                if isinstance(npc, ErikaChickenGirl):
                    state.npcs.remove(npc)
                    state.player.canMove = True
                    print(state.player.canMove)
                    Treasure.add_quest_to_player(state.player, Treasure.INVITATION)

        for treasurechest in state.treasurechests:
            treasurechest.update(state)

        if controller.isExitPressed is True:
            state.isRunning = False




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

        for treasurechest in state.treasurechests:
            treasurechest.draw(state)



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
