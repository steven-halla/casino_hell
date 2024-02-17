import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.demon.demon7 import Demon7
from entity.npc.battle_screen.rest_area_teleporter import RestScreenTeleporter
from entity.npc.chilli_screen.bobby_bibs import BobbyBibs
from entity.npc.chilli_screen.brutal_patrick import BrutalPatrick
from entity.npc.chilli_screen.chilly_billy import ChillyBilly
from entity.npc.chilli_screen.hedgeMazeTeleporter import HedgeMazeScreenTeleporter
from entity.npc.chilli_screen.jessica_starving import JessicaStarving
from entity.npc.chilli_screen.rest_screen_teleporter import RestScreenFromChilliScreenTeleporter
from entity.npc.chilli_screen.rumble_bill import RumbleBill
from entity.npc.chilli_screen.sir_leopold_the_hedgehog import SirLeopoldTheHedgeHog
from entity.npc.sleepy_ned import SleepyNed
from entity.npc.hedge_maze_screen.hedgehog1 import HedgeHog1
from entity.npc.hedge_maze_screen.hedgehog2 import HedgeHog2
from entity.npc.hedge_maze_screen.hedgehog3 import HedgeHog3
from entity.npc.hedge_maze_screen.hedgehog4 import HedgeHog4
from entity.npc.inn_guard import InnGuard
from entity.npc.nurgle import Nurgle
from entity.player.player import Player
from screen.examples.screen import Screen
from physics.rectangle import Rectangle


class ChilliScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/chilli.tmx")
        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.player = Player(333, 555)
        self.hedge_hog_counter = 4
        self.npcs = []
        self.move_player_down_flag = False

        self.music_file = "/Users/stevenhalla/code/casino_hell/assets/music/chili_screen.mp3"

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
        # self.initialize_music()
        super().start(state)
        # state.npcs.clear()
        # state.demons.clear()
        print("The demons are: " + str(state.demons))

        if "blue flower" in state.player.items:
            # Loop through the demons to find Demon7 by its position or a unique identifier
            for demon in list(state.demons):  # Make a copy of the list to modify it while iterating
                if isinstance(demon, Demon7):
                    state.demons.remove(demon)
                    break  # Exit the loop once the Demon7 instance is found and removed
        # state.demons = []


        if state.rest_area_to_chili_area_entry_point == True:
            player_start_x = 16 * 5  # Desired X coordinate
            player_start_y = 16 * 5  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.rest_area_to_chili_area_entry_point = False

        # Check if a player instance already exists
        # if not hasattr(state, 'player') or state.player is None:
        #     player_start_x = 300
        #     player_start_y = 200
        #     state.player = Player(player_start_x, player_start_y)

        state.npcs.clear()
        state.demons.clear()

        state.treasurechests = [

            # WaterBottle(16 * 36, 16 * 10),

        ]



        state.npcs = []

        # Add other NPCs to the state.npcs list
        state.npcs.extend([
            BobbyBibs(16 * 37, 16 * 18),
            BrutalPatrick(16 * 30, 16 * 5),
            ChillyBilly(16 * 12, 16 * 23),
            JessicaStarving(16 * 4, 16 * 30),
            SirLeopoldTheHedgeHog(16 * 18, 16 * 26),
            HedgeMazeScreenTeleporter(16 * 4, 16 * 8),
            RestScreenFromChilliScreenTeleporter(16 * 35, 16 * 34),
            RumbleBill(16 * 12, 16 * 12),

            # SleepyNed(16 * 18, 16 * 26),
        ])



        state.demons = [
            # Demon1(16 * 55, 16 * 3),

        ]

    def update(self, state: "GameState"):
        state.demons.clear()

        # print("The demons are: " + str(state.demons))
        #
        # print(str(state.player.items))
        # print(str(state.player.money))

        if state.maze_area_to_chili_area_entry_point == True:
            player_start_x = 16 * 5  # Desired X coordinate
            player_start_y = 16 * 5  # Desired Y coordinate
            state.player.setPosition(player_start_x, player_start_y)
            state.maze_area_to_chili_area_entry_point = False

        if "blue flower" in state.player.items:
            # Loop through the NPCs to find SirLeopoldTheHedgeHog and update his position
            for npc in state.npcs:
                if isinstance(npc, SirLeopoldTheHedgeHog):
                    # Update SirLeopoldTheHedgeHog's position to the new coordinates
                    npc.setPosition(16 * 35, 16 * 32)
                    break  # Break the loop once SirLeopoldTheHedgeHog is found and moved

        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()
        for npc in state.npcs:
            npc.update(state)
            if isinstance(npc, Nurgle) and npc.to_be_deleted:
                state.npcs.remove(npc)

        for npc in state.npcs:
            if isinstance(npc, SirLeopoldTheHedgeHog) and npc.vanish:
                state.npcs.remove(npc)

        for npc in state.npcs:
            if isinstance(npc, SirLeopoldTheHedgeHog) and "sir leopold" in state.player.companions:
                state.npcs.remove(npc)

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
