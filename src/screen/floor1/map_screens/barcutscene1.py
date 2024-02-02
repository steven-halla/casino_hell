import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.npc.battle_screen.Guy import Guy
from entity.npc.boss_screen.FlippingSandy import FlippingSandy
from entity.npc.boss_screen.black_jack_jared import BlackJackJared
from entity.npc.boss_screen.opossum_in_a_can_ichi import IchiOpossum
from entity.npc.chilli_screen.sir_leopold_the_hedgehog import SirLeopoldTheHedgeHog
from entity.npc.hedge_maze_screen.hedgehog1 import HedgeHog1
from entity.npc.hedge_maze_screen.hedgehog2 import HedgeHog2
from entity.npc.hedge_maze_screen.hedgehog3 import HedgeHog3
from entity.npc.hedge_maze_screen.hedgehog4 import HedgeHog4
from entity.npc.rest_screen.bar_keep import BarKeep
from entity.npc.rest_screen.bar_keep_low_body import BarKeepLowBody
from entity.npc.rest_screen.chili_pit_teleporter import ChiliPitTeleporter
from entity.npc.rest_screen.doctor_opossum import DoctorOpossum
from entity.npc.chilli_screen.hedgeMazeTeleporter import HedgeMazeScreenTeleporter
from entity.npc.rest_screen.inn_keeper import InnKeeper
from entity.npc.rest_screen.justin_no_fruit import JustinNoFruit
from entity.npc.rest_screen.new_teleporter import NewTeleporter
from entity.npc.rest_screen.quest_giver_janet import QuestGiverJanet

from entity.npc.rest_screen.start_screen_teleporter import StartScreenTeleporter
from entity.npc.rest_screen.suffering_suzy import SufferingSuzy
from entity.npc.rest_screen.wally_guide import WallyGuide
from entity.npc.inn_guard import InnGuard
from entity.npc.nurgle import Nurgle
from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.player.player import Player
from entity.treasurechests.powerpotion import PowerPotion
from screen.examples.screen import Screen
from physics.rectangle import Rectangle



class BarCutScene1Screen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.chili_pit_flag = False
        self.tiled_map = pytmx.load_pygame("./assets/map/casinomaingame5.tmx")
        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.player = Player(333, 555)
        self.hedge_hog_counter = 0
        move_player_down_flag = False
        self.npcs = []  # Initialize the NPCs list as empty
        self.rest_screen_npc_janet_talk_first_five_hundred = False
        self.rest_screen_npc_janet_quest_2_counter = False
        self.rest_screen_npc_janet_quest_3_counter = False
        self.rest_screen_npc_janet_find_hog = False


        self.npc_janet_textbox2 = False
        self.npc_janet_textbox3 = False
        self.npc_janet_textbox4 = False
        self.npc_janet_textbox5 = False
        self.npc_janet_textbox6 = False

        self.nurgle_the_hedge_hog = True

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
        self.stop_music()
        self.initialize_music()
        super().start(state)

        # Check if a player instance already exists
        if not hasattr(state, 'player') or state.player is None:
            player_start_x = 300
            player_start_y = 200
            state.player = Player(player_start_x, player_start_y)


        # state.npcs = []
        state.npcs = [

            SirLeopoldTheHedgeHog(16 * 11, 16 * 30),
            QuestGiverJanet(16 * 21, 16 * 20),
            BarKeep(16 * 31, 16 * 10),
            CindyLongHair(16 * 31, 16 * 20),
            Guy(16 * 31, 16 * 28)

        ]




    def update(self, state: "GameState"):
        state.player.canMove = False
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

        for npc in state.npcs:
            npc.draw(state)


        state.obstacle.draw(state)

        state.player.draw(state)

        # Update the display
        pygame.display.update()
