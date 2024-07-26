import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.demon.demon1 import Demon1
from entity.npc.area2.area_2_start_screen.alice import Alice
from entity.npc.hedge_maze_screen.evilcat import EvilCat
from entity.npc.hedge_maze_screen.hedgehog1 import HedgeHog1
from entity.npc.hedge_maze_screen.hedgehog2 import HedgeHog2
from entity.npc.hedge_maze_screen.hedgehog3 import HedgeHog3
from entity.npc.hedge_maze_screen.hedgehog4 import HedgeHog4
from entity.npc.rest_screen.bar_keep import BarKeep
from entity.npc.rest_screen.bar_keep_low_body import BarKeepLowBody
from entity.npc.rest_screen.boss_teleporter import BossTeleporter
from entity.npc.rest_screen.chili_pit_teleporter import ChiliPitTeleporter
from entity.npc.rest_screen.doctor_opossum import DoctorOpossum
from entity.npc.rest_screen.inn_keeper import InnKeeper
from entity.npc.rest_screen.justin_no_fruit import JustinNoFruit
from entity.npc.rest_screen.new_teleporter import NewTeleporter

from entity.npc.rest_screen.start_screen_teleporter import StartScreenTeleporter
from entity.npc.rest_screen.suffering_suzy import SufferingSuzy
from entity.npc.rest_screen.wally_guide import WallyGuide
from entity.npc.inn_guard import InnGuard
from entity.npc.nurgle import Nurgle
from entity.player.player import Player
from entity.treasurechests.blueflower import BlueFlower
from entity.treasurechests.powerpotion import PowerPotion
from screen.examples.screen import Screen
from physics.rectangle import Rectangle



class Area2RestScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.chili_pit_flag = False
        self.tiled_map = pytmx.load_pygame("./assets/map/restarea.tmx")
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



        self.music_file =  "/Users/stevenhalla/code/casino_hell/assets/music/relax_screen.mp3"

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


        if state.start_area_to_rest_area_entry_point == True:
            player_start_x = 16 * 94  # Desired X coordinate
            player_start_y = 16 * 3  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.start_area_to_rest_area_entry_point = False
        elif state.gambling_area_to_rest_area_entry_point == True:
            player_start_x = 44 * 6 # Desired X coordinate
            player_start_y = 16 * 3  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.gambling_area_to_rest_area_entry_point = False
        elif state.chili_area_to_rest_area_entry_point == True:
            player_start_x = 16 * 14  # Desired X coordinate
            player_start_y = 16 * 46  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.chili_area_to_rest_area_entry_point = False

        self.inn_badge_recieved_tracker = True




        if state.player.hasRabies:
            state.player.stamina_points = 1

        if state.coinFlipFredScreen.coinFlipFredMoney < 10:
            state.coinFlipFredScreen.coinFlipFredDefeated = True

        if state.coinFlipTedScreen.coinFlipTedMoney < 10:
            state.coinFlipTedScreen.coinFlipTedDefeated = True

        if state.blackJackThomasScreen.cheater_bob_money < 10:
            state.blackJackThomasScreen.black_jack_thomas_defeated = True

        if state.blackJackRumbleBillScreen.cheater_bob_money < 10:
            state.blackJackRumbleBillScreen.black_jack_rumble_bill_defeated = True


        if state.opossumInACanNellyScreen.nellyOpossumMoney < 10:
            state.opossumInACanNellyScreen.nellyOpossumIsDefeated = True

        if state.opossumInACanSallyScreen.sallyOpossumMoney < 10:
            state.opossumInACanSallyScreen.sallyOpossumIsDefeated = True

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

        state.treasurechests = [

            # WaterBottle(16 * 36, 16 * 10),

        ]
        # Check the value of state.player.body

        # state.npcs = []
        state.npcs = [npc for npc in state.npcs if not isinstance(npc, (BarKeep, BarKeepLowBody))]

        state.npcs = [
            Alice(16 * 24, 16 * 33),
            # Johnathon(16 * 30, 16 * 33),
            # Nibblet(16 * 40, 16 * 33),
            # Alex(16 * 16, 16 * 45),
            # Lunky(16 * 26, 16 * 45),
            # Natasha(16 * 36, 16 * 45),
            # MCNugg(16 * 45, 16 * 45),
            # OpossumInACanCandy(16 * 55, 16 * 45),
            # CoinFlipBetty(16 * 55, 16 * 35),

        ]

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
