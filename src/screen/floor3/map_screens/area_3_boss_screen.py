import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.npc.area1.area_1_boss_screen.area_1_boss_to_gambling_door import Area1BossToGamblingDoor
from entity.npc.area1.area_1_gamble_screen.area_1_gambling_to_maze_door import Area1GamblingToMazeDoor
from entity.npc.area1.area_1_gamble_screen.area_1_gambling_to_rest_door import Area1GamblingToRestDoor
from entity.npc.area1.area_1_rest_screen.area_1_inn_keeper import Area1InnKeeper
from entity.npc.area1.area_1_rest_screen.area_1_rest_to_intro_door import Area1RestToIntroDoor
from entity.npc.area1.area_1_rest_screen.cody_talk import CodyTalk
from entity.npc.area1.area_1_start_screen.anna_quest import AnnaQuest
from entity.npc.area1.area_1_start_screen.coin_flip_ted import CoinFlipTed
from entity.npc.area1.area_1_start_screen.mike_talk import MikeTalk
from entity.npc.area1.area_1_start_screen.patrick_talk import PatrickTalk
from entity.npc.area3.area_3_boss_screen.area_3_boss_to_gambling_screen import Area3BossToGamblingDoor
from entity.npc.area5.area_5_rest_screen_trash.black_jack_fengus import BlackJackFengus
from entity.npc.area5.area_5_rest_screen_trash.coin_flip_wanton import CoinFlipWanton
from entity.npc.area5.area_5_rest_screen_trash.craps_wimpleton import CrapsWimpleton
from entity.npc.area5.area_5_rest_screen_trash.hangry_angry_hippos_nippy import HangryAngryHipposNippy
from entity.npc.area5.area_5_rest_screen_trash.opossum_in_a_can_bubba import OpossumInACanBubba
from entity.npc.area5.area_5_rest_screen_trash.slots_burbadan import SlotsBurbadan

from entity.player.player import Player

from screen.examples.screen import Screen
from physics.rectangle import Rectangle
from screen.floor5.battle_screens.coin_flip_wanton_screen import CoinFlipWantonScreen
from screen.floor5.battle_screens.craps_wimpleton_screen import CrapsWimpletonScreen
from screen.floor5.battle_screens.hungry_starving_hippos_nippy_screen import HungryStarvingHipposNippyScreen
from screen.floor5.battle_screens.opossum_in_a_can_bubba_screen import OpossumInACanBubbaScreen
from screen.floor5.battle_screens.slots_burbadan_screen import SlotsBurbadanScreen


class Area3BossScreen(Screen):
# WHAT IF I CALL START AFTER EXITING A SCREEN TO CALL IMPORTANT FUNS WHILE NOT ALWAYS USING UPDATE
    def __init__(self):
        super().__init__("Casino MainScreen")
        self.chili_pit_flag = False
        self.tiled_map = pytmx.load_pygame("./assets/map/rest_area_3_final_map.tmx")
        # self.tiled_map = pytmx.load_pygame("./assets/map/restarea.tmx")
        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.player = Player(333, 555)
        move_player_down_flag = False
        self.npcs = []  # Initialize the NPCs list as empty
        self.clock = pygame.time.Clock()  # Initialize the clock
        self.music_file = "./assets/music/relax_screen.mp3"

        self.music_volume = 0.5  # Adjust as needed
        self.initialize_music()
        self.shop_lock = False

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
            player_start_x = 16 * 33
            player_start_y = 16 * 26
            state.player.setPosition(player_start_x, player_start_y)
        state.player.canMove = True


        state.treasurechests = []
        self.stop_music()
        # if state.musicOn:
        #     self.initialize_music()
        super().start(state)
        state.npcs.clear()

        # if (state.player.perception >= 1
        #         and Treasure.FIVE_HUNDRED_GOLD.value not in state.player.level_two_npc_state):
        #     state.treasurechests = [
        #         Area3MoneyBag(16 * 97, 14 * 55),
        #     ]
        #
        # if state.player.perception >= 2 and Treasure.FOCUS_BOOST.value not in state.player.level_two_npc_state:
        #     state.treasurechests.append(Area3FocusBoost(16 * 111, 14 * 111))

        state.npcs = [

            Area3BossToGamblingDoor(16 * 30, 16 * 25),
            # Area1GamblingToMazeDoor(16 * 45, 16 * 40),

        ]

    def update(self, state: "GameState"):
        # In your update() function (or in a function that's called every frame):



        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()

        for npc in state.npcs:
            npc.update(state)

        state.treasurechests = [chest for chest in state.treasurechests if not chest.remove]

        for treasurechest in state.treasurechests:
            treasurechest.update(state)

        player.update(state)

        # Check map for collision
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

        # 1. Draw all NPCs normally
        for npc in state.npcs:
            npc.draw(state)  # Not skipping any

        # 2. Then draw only the dialog box for the talking one
        for npc in state.npcs:
            if npc.state == "talking":
                npc.draw(state, only_dialog=True)

        for treasurechest in state.treasurechests:
            treasurechest.draw(state)



        state.obstacle.draw(state)
        if state.player.hide_player == False:
            state.player.draw(state)

        # Enter the menu ONCE when pressing start (P)
        # Only enter the menu if currently not in one
        # Only enter menu if not already in any screen
        if state.player.current_screen == "" and state.controller.start_button:
            state.player.current_screen = "main_menu_screen"
            state.player.canMove = False

        # If in any menu-related screen, just draw the player menu logic
        if state.player.current_screen.endswith("_screen"):
            state.player.draw_player_stats(state)



            # if state.controller.isBPressed or state.controller.isBPressedSwitch and state.player.current_screen == "main_menu_screen":
            #     if state.controller.isPPressed or state.controller.isXPressedSwitch:
            #         state.player.canMove = True
            #         state.player.menu_paused = False
            #
            #         state.controller.isPPressed = False
            #         state.controller.isXPressedSwitch = False
            #         return

        # Update the display
        pygame.display.update()
