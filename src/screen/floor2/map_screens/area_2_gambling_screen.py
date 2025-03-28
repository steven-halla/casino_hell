import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.npc.area2.area_2_gambling_screen.area_2_gambling_to_rest_area import Area2GamblingToRestArea
from entity.npc.area2.area_2_gambling_screen.black_jack_mack import BlackJackMack
from entity.npc.area2.area_2_gambling_screen.coin_flip_betty import CoinFlipBetty
from entity.npc.area2.area_2_gambling_screen.happy_craps import CrapsHappy
from entity.npc.area2.area_2_gambling_screen.lunky import Lunky
from entity.npc.area2.area_2_gambling_screen.nibblet import Nibblet
from entity.npc.area2.area_2_gambling_screen.slots_rippa_snappa import SlotsRippaSnappa
from entity.npc.area2.area_2_gambling_screen.opossum_in_a_can_candy import OpossumInACanCandy
from entity.npc.area2.area_2_rest_screen.Natalie import Natalie

from entity.player.player import Player
from entity.treasurechests.bbqsauce import BBQSauce
from game_constants.events import Events
from screen.examples.screen import Screen
from physics.rectangle import Rectangle



class Area2GamblingScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.chili_pit_flag = False
        self.tiled_map = pytmx.load_pygame("./assets/map/gambling_area_level_2.tmx")
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

        self.music_file = "./assets/music/town_music.mp3"
        self.music_volume = 0.5  # Adjust as needed
        self.initialize_music()



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
        print("jdfsajf;dsjfjsa;jlsajf;asfj;sjfljas;fjlksajfl;kajs;klfjdslf;ldjsa")
        self.stop_music()


        state.treasurechests = [


        ]

        print("this is for our start area")
        print(str(state.area_2_rest_area_to_gambling_point))

        if (Events.QUEST_1_COIN.value in state.player.level_two_npc_state and
                Events.QUEST_1_BADGE.value in state.player.level_two_npc_state and
                Events.QUEST_1_COMPLETE.value not in state.player.level_two_npc_state):
            print("yoyoyo")
            state.player.level_two_npc_state.append(Events.QUEST_1_COMPLETE.value)

        # state.area_2_gambling_area_to_rest_point = True

        if state.area_2_gambling_area_to_rest_point == True:
            print("hdshfa;ljflksja;f")
            player_start_x = 16 * 37  # Desired X coordinate
            player_start_y = 16 * 34  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.area_2_gambling_area_to_rest_point = False




        self.stop_music()
        if state.musicOn == True:
            self.initialize_music()
        super().start(state)
        state.npcs.clear()

        # Check if a player instance already exists
        # if not hasattr(state, 'player') or state.player is None:
        #     player_start_x = 300
        #     player_start_y = 200
        #     state.player = Player(player_start_x, player_start_y)


        # Check the value of state.player.body
        print("Level 2 npc state :" + str(state.player.level_two_npc_state))


        if (Events.MC_NUGGET_QUEST_1_REWARD.value in state.player.level_two_npc_state
                and state.player.perception >= 2
                and Events.MC_NUGGET_SECOND_QUEST_COMPLETE.value not in state.player.level_two_npc_state):
            print("ydddle")


            state.treasurechests = [

                BBQSauce(16 * 55, 14 * 42),

            ]

        # state.npcs = []


        state.npcs = [
            BlackJackMack(16 * 110, 16 * 7),

            OpossumInACanCandy(16 * 9, 16 * 9),

            CoinFlipBetty(16 * 36, 16 * 6),

            SlotsRippaSnappa(16 * 61, 16 * 7),

            CrapsHappy(16 * 81, 16 * 5),

            Nibblet(16 * 20, 16 * 31),
            Lunky(16 * 60, 16 * 28),
            Area2GamblingToRestArea(16 * 36, 16 * 39)

        ]

    def update(self, state: "GameState"):
        # delta_time = self.clock.tick(60)  # 60 FPS cap
        # fps = 1000 / delta_time
        # print(fps)



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



        state.treasurechests = [chest for chest in state.treasurechests if not chest.remove]


        for treasurechests in state.treasurechests:
            treasurechests.update(state)






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
