import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.demon.demon1 import Demon1
from entity.demon.demon10 import Demon10
from entity.demon.demon6 import Demon6
from entity.demon.demon7 import Demon7
from entity.demon.demon8 import Demon8
from entity.demon.demon9 import Demon9
from entity.npc.area2.area_2_gambling_screen.area_2_gambling_to_rest_area import Area2GamblingToRestArea
from entity.npc.area2.area_2_gambling_screen.black_jack_mack import BlackJackMack
from entity.npc.area2.area_2_gambling_screen.coin_flip_betty import CoinFlipBetty
from entity.npc.area2.area_2_gambling_screen.happy_craps import CrapsHappy
from entity.npc.area2.area_2_gambling_screen.lunky import Lunky
from entity.npc.area2.area_2_gambling_screen.nibblet import Nibblet
from entity.npc.area2.area_2_gambling_screen.slots_rippa_snappa import SlotsRippaSnappa
from entity.npc.area2.area_2_gambling_screen.opossum_in_a_can_candy import OpossumInACanCandy
from entity.npc.area2.area_2_nugget_screen.area_2_nugget_to_rest_area import Area2NuggetToRestArea
from entity.npc.area2.area_2_nugget_screen.mcnugget import MCNugg
from entity.npc.area2.area_2_rib_demon_maze_screen.switch_6 import Switch6
from entity.npc.area2.area_2_rib_demon_maze_screen.switch_7 import Switch7
from entity.npc.area2.area_2_rib_demon_maze_screen.switch_8 import Switch8

from entity.player.player import Player
from entity.treasurechests.nuggie_sauce_ingrediant_1 import NuggieSauceIngrediant1
from entity.treasurechests.slots_vest import SlotsVest
from game_constants.events import Events
from game_constants.treasure import Treasure
from screen.examples.screen import Screen
from physics.rectangle import Rectangle



class Area2RibDemonMazeScreen3(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.chili_pit_flag = False
        self.tiled_map = pytmx.load_pygame("./assets/map/ribdemonhideroom3.tmx")
        self.y_up_move = False
        self.powerpotiongotten = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.player = Player(333, 555)
        self.hedge_hog_counter = 0
        move_player_down_flag = False
        self.npcs = []  # Initialize the NPCs list as empty
        self.poison_counter = 0
        self.clock = pygame.time.Clock()  # Initialize the clock
        self.penalty_poison_counter = 5
        self.buy_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/BFBuyingSelling.wav")  # Adjust the path as needed
        self.buy_sound.set_volume(0.3)

        self.cant_buy_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/cantbuy3.wav")  # Adjust the path as needed
        self.cant_buy_sound.set_volume(0.5)


        # self.music_file =  "/Users/stevenhalla/code/casino_hell/assets/music/relax_screen.mp3"
        #
        # self.music_volume = 0.5  # Adjust as needed
        # self.initialize_music()
        self.total_elapsed_time = 0  # Total elapsed time in milliseconds
        self.last_interval_count = 0  # Number of 5-second intervals that have passed
        self.player_hiding = False
        self.rally_point = (16 * 85, 16 * 10)  # Set the rally point here
        self.switch_6_on = False
        self.switch_7_on = False
        self.switch_8_on = False
        self.all_switches_on = False

        self.player_caught = False
        self.maze_3 = True


    # def stop_music(self):
    #     pygame.mixer.music.stop()
    #
    # def initialize_music(self):
    #     # Initialize the mixer
    #     pygame.mixer.init()
    #
    #     # Load the music file
    #     pygame.mixer.music.load(self.music_file)
    #
    #     # Set the volume for the music (0.0 to 1.0)
    #     pygame.mixer.music.set_volume(self.music_volume)
    #
    #     # Play the music, -1 means the music will loop indefinitely
    #     pygame.mixer.music.play(-1)

    def start(self, state: "GameState"):
        self.player_caught = False

        print("this is for our nuggy area")
        print(str(state.area_2_rest_area_to_gambling_point))
        # state.area_2_rest_area_to_rib_demon_maze_point = True

        state.area_2_rest_area_to_rib_demon_maze_point3 = True

        if state.area_2_rest_area_to_rib_demon_maze_point3 == True:
            print("nuggggggggggggggg;f")
            player_start_x = 16 * 5  # Desired X coordinate
            player_start_y = 16 * 10 # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.area_2_rest_area_to_rib_demon_maze_point = False



        #t
        super().start(state)
        state.npcs.clear()
        state.treasurechests.clear()

        # Check if a player instance already exists
        # if not hasattr(state, 'player') or state.player is None:
        #     player_start_x = 300
        #     player_start_y = 200
        #     state.player = Player(player_start_x, player_start_y)
        #
        if Events.NUGGIE_SAUCE_1_FOUND.value not in state.player.level_two_npc_state:
            state.treasurechests = [
                NuggieSauceIngrediant1(16* 95, 16 * 95)
            ]
        #
        # if (Events.SLOTS_VEST_FOUND.value not in state.player.level_two_npc_state
        #         and state.player.perception > 2):
        #     state.treasurechests = [
        #     SlotsVest(16 * 29, 16 * 35),
        #
        #
        # ]



        state.demons = [
            #
            Demon10(16 * 85, 16 * 10)

            # Demon3(16 * 20, 14 * 85),
            # Demon4(16 * 20, 14 * 10),
            # Demon3(16 * 20, 14 * 76),
            # Demon2(16 * 55, 16 * 13),
            # Demon3(16 * 55, 16 * 23),
            # Demon4(16 * 55, 16 * 33),
        ]


        # Check the value of state.player.body

        state.npcs = [
            Switch6(16 * 96, 16 * 5),
            Switch7(16 * 58, 16 * 57),
            Switch8(16 * 20, 16 * 94)
        ]

        # state.npcs = [
        #     MCNugg(16 * 15, 16 * 5),
        #     Area2NuggetToRestArea(16 * 35, 16 * 34),
        #
        # ]

    def update(self, state: "GameState"):
        delta_time = self.clock.tick(60)  # 60 FPS cap

        if self.player_caught == True:
            state.area_2_rest_area_to_rib_demon_maze_point3 = True
            state.currentScreen = state.area2RibDemonMazeScreen3
            state.area2RibDemonMazeScreen3.start(state)
            self.player_caught = False

        if self.switch_6_on and self.switch_7_on and self.switch_8_on:
            self.all_switches_on = True





        # Update the total elapsed time
        self.total_elapsed_time += delta_time

        # Calculate the current interval count using integer division
        current_interval_count = self.total_elapsed_time // 5000  # 5000 ms = 5 seconds

        # Check if a new 5-second interval has started
        if current_interval_count > self.last_interval_count:
            print("5 seconds have passed")
            state.player.stamina_points -= 4
            self.last_interval_count = current_interval_count


        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()




        for npc in state.npcs:
            npc.update(state)


        for demon in state.demons:
            demon.update(state)

        for treasure in state.treasurechests:
            treasure.update(state)









        if controller.isExitPressed is True:
            state.isRunning = False






        player.update(state)

        # check map for collision
        if self.tiled_map.layers:
            tile_rect = Rectangle(0, 0, 16, 16)
            collision_layer = self.tiled_map.get_layer_by_name("collision")
            # teleport_layer = self.tiled_map.get_layer_by_name("teleport")
            #
            # for x, y, image in teleport_layer.tiles():
            #     tile_rect.x = x * 16
            #     tile_rect.y = y * 16
            #
            #     if state.player.collision.isOverlap(tile_rect):
            #         state.area_2_rest_area_to_rib_demon_maze_point2 = True
            #         state.currentScreen = state.area2RibDemonMazeScreen2
            #         state.area2RibDemonMazeScreen2.start(state)
            #
            #         print("They want you as a new recruit")


            for x, y, image in collision_layer.tiles():
                tile_rect.x = x * 16
                tile_rect.y = y * 16


                if state.player.collision.isOverlap(tile_rect):
                    state.player.undoLastMove()
                for demon in state.demons:

                    if demon.collision.isOverlap(tile_rect):
                        demon.undoLastMove()
                        if demon.facing_left == True:
                            demon.facing_left = False
                            demon.facing_right = True
                        elif demon.facing_right == True:
                            demon.facing_right = False
                            demon.facing_left = True
                        elif demon.facing_up == True:
                            demon.facing_up = False
                            demon.facing_down = True
                        elif demon.facing_down == True:
                            demon.facing_down = False
                            demon.facing_up = True

            hide_layer = self.tiled_map.get_layer_by_name("hide")

            for x, y, image in hide_layer.tiles():
                tile_rect.x = x * 16
                tile_rect.y = y * 16
                if state.player.collision.isOverlap(tile_rect):
                    self.player_hiding = True
                    # for demon in state.demons:
                    #     if isinstance(demon, Demon10):
                    #         demon.move_to_rally()

            main_layer = self.tiled_map.get_layer_by_name("bg")

            for x, y, image in main_layer.tiles():
                tile_rect.x = x * 16
                tile_rect.y = y * 16
                if state.player.collision.isOverlap(tile_rect):

                    self.player_hiding = False



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

            hiding_layer = self.tiled_map.get_layer_by_name("hide")
            for x, y, image in hiding_layer.tiles():
                pos_x = x * tile_width + state.camera.x
                pos_y = y * tile_height + state.camera.y

                scaled_image = pygame.transform.scale(image,(
                    tile_width * 1.3, tile_height * 1.3))

                state.DISPLAY.blit(scaled_image, (pos_x, pos_y))



        for npc in state.npcs:
            npc.draw(state)

        for demon in state.demons:
            demon.draw(state)

        for treasure in state.treasurechests:
            treasure.draw(state)



        state.obstacle.draw(state)

        if self.player_hiding == False:
            state.player.draw(state)



        # if state.controller.isPPressed == True:
        #
        #     state.player.draw_player_stats(state)
        #
        #     if state.controller.isBPressed == True:
        #         if state.controller.isPPressed:
        #             state.controller.isPPressed = False
        #             return

        font = pygame.font.Font(None, 36)

        # Step 2: Render the player's stamina points as text
        stamina_text = font.render(f"HP: {state.player.stamina_points} ", True, (177, 255, 255))  # White color

        # Step 3: Blit the text on the display at (50, 50)
        state.DISPLAY.blit(stamina_text, (50, 50))

        # Update the display
        pygame.display.update()
