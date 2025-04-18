import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, BLACK, WHITE

from entity.npc.start_screen.bapping_mike import BappingMike
from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.npc.start_screen.flippin_ted import FlippinTed
from entity.npc.start_screen.hungry_patrick import HungryPatrick
from entity.npc.nurgle import Nurgle
from entity.npc.start_screen.main_screen_teleporter import MainScreenTeleporter
from screen.examples.screen import Screen
from physics.rectangle import Rectangle


class StartScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/startscreen1.tmx")
        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.hedge_hog_counter = 0
        self.lock_screen = False


        # self.music_file = "./assets/music/town_music.mp3"
        # self.music_volume = 0.5  # Adjust as needed
        # self.initialize_music()

        self.clock = pygame.time.Clock()  # Initialize the clock


    def stop_music(self):
        pygame.mixer.music.stop()

    def initialize_music(self):
        pass
        # Initialize the mixer
        # pygame.mixer.init()
        #
        # # Load the music file
        # pygame.mixer.music.load(self.music_file)
        #
        # # Set the volume for the music (0.0 to 1.0)
        # pygame.mixer.music.set_volume(self.music_volume)
        #
        # # Play the music, -1 means the music will loop indefinitely
        # pygame.mixer.music.play(-1)

    def start(self, state: "GameState"):
        self.stop_music()
        if state.musicOn == True:
            pass
            # self.initialize_music()
        super().start(state)
        # self.show_loading_screen(state)

        if state.start_new_game_entry_point == True:
            player_start_x = 16 * 33  # Desired X coordinate
            player_start_y = 16 * 26  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.start_new_game_entry_point = False
        elif state.rest_area_to_start_area_entry_point == True:
            player_start_x = 44 * 18.5 # Desired X coordinate
            player_start_y = 16 * 4  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.rest_area_to_start_area_entry_point = False



        state.npcs = [

            BappingMike(16* 18, 16 * 22),
            HungryPatrick(16* 41, 16 * 22),
            # InnGuard(16* 35, 16 * 15),
            # NickyHints(16* 25, 16 * 25),
            MainScreenTeleporter(16 * 52, 16 * 0),
            FlippinTed(16* 5, 16 * 5),



             CindyLongHair(16 * 36, 16 * 44),

                      ]


    def update(self, state: "GameState"):

        start_time = pygame.time.get_ticks()

        # ... [your game update logic]
        self.clock.tick(60)


        # timer = self.clock.tick(60)
        # print("Your start screen game clock is: " + str(timer))
        end_time = pygame.time.get_ticks()


        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()
        for npc in state.npcs:
            npc.update(state)
            if isinstance(npc, Nurgle) and npc.to_be_deleted:
                state.npcs.remove(npc)
                print("removed")

        # Assuming you have your hedgehog instances named like HedgeHog1, HedgeHog2, etc.
        # hedgehogs = [HedgeHog1(), HedgeHog2(), HedgeHog3(), HedgeHog4()]


        ### i can use this to append NPC if i need to , just state.npcs.append(npc)
        # for npc in state.npcs:
        #     npc.update(state)
        #     # Check if the npc is any of the hedgehogs
        #     if isinstance(npc, (HedgeHog1, HedgeHog2, HedgeHog3, HedgeHog4)) and npc.to_be_deleted:
        #         self.hedge_hog_counter += 1
        #         print(self.hedge_hog_counter)
        #         state.npcs.remove(npc)

        # Game Update Loop
        # for chest in state.treasurechests:
        #     chest.update(state)

        # for demon in state.demons:
        #     demon.update(state)
        #     if demon.move_player_down:
        #         state.player.collision.y += 100  # Move player down by 100 pixels
        #         demon.move_player_down = False

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

        #player position
        state.camera.x = PLAYER_OFFSET[0] - state.player.collision.x
        state.camera.y = PLAYER_OFFSET[1] - state.player.collision.y



    def draw(self, state: "GameState"):
        # self.show_loading_screen(state)
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

        # for demon in state.demons:
        #     demon.draw(state)
        #
        # for treasurechests in state.treasurechests:
        #     treasurechests.draw(state)

        # state.obstacle.draw(state)


        # state.player.draw(state)
        state.player.draw(state)


        if state.controller.isPPressed == True:

            state.player.draw_player_stats(state)

            if state.controller.isBPressed == True:
                if state.controller.isPPressed:
                    state.controller.isPPressed = False
                    return
        pygame.display.update()

    # def show_loading_screen(self, state):
    #     current_time = pygame.time.get_ticks()
    #     if current_time - start_time < 3000:  # Check if less than 3 seconds have passed
    #         state.DISPLAY.fill(BLACK)  # Fill the screen with black
    #
    #         font = pygame.font.Font(None, 36)  # Setup the font
    #         text_surface = font.render('Loading...', True, WHITE)  # Create the text surface
    #
    #         # Calculate the position for the text to center it on the screen
    #         text_x = (SCREEN_WIDTH - text_surface.get_width()) // 2
    #         text_y = (SCREEN_HEIGHT - text_surface.get_height()) // 2
    #
    #         # Blit the text surface to the display at the calculated position
    #         state.DISPLAY.blit(text_surface, (text_x, text_y))
    #
    #         # Update the display to show the text
    #         pygame.display.update()
    #     else:
    #         # Optional: Code to transition away from the loading screen after 3 seconds
    #         pass
    #
    #     # Update the display
    #     pygame.display.update()
