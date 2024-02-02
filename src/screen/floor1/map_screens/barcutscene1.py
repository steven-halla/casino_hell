import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.gui.textbox.npc_text_box import NpcTextBox
from entity.npc.battle_screen.Guy import Guy

from entity.npc.chilli_screen.sir_leopold_the_hedgehog import SirLeopoldTheHedgeHog

from entity.npc.rest_screen.bar_keep import BarKeep

from entity.npc.rest_screen.quest_giver_janet import QuestGiverJanet

from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.player.player import Player
from screen.examples.screen import Screen
from physics.rectangle import Rectangle



class BarCutScene1Screen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/casinomaingame5.tmx")

        self.player = Player(333, 555)
        move_player_down_flag = False
        self.npcs = []
        self.initial_player_y = None  # To store the initial Y position of the player


        self.timer = 0  # Timer to track time since the screen started
        self.player_moved = False  # Flag to track if the player has been moved
        self.move_distance = 30  # Distance to move the player during the cutscene







        self.music_file =  "/Users/stevenhalla/code/casino_hell/assets/music/relax_screen.mp3"

        self.music_volume = 0.5  # Adjust as needed
        self.initialize_music()

        self.cut_scene_1_messages = {
            "message_1": NpcTextBox(
                [
                    "Guy: Most people here are here to gamble, you can quit a match and go rest if you feel it too much.",

                ],
                (50, 450, 50, 45), 30, 500
            ),
            "message_2": NpcTextBox(
                ["Bro, you look totally sick, go see the doctor ASAP"],
                (50, 450, 700, 130), 36, 500
            ),
            "message_3": NpcTextBox(
                ["bro you look sic go see...oh wait your not longer sic never mind"],
                (50, 450, 700, 130), 36, 500
            ),
        }

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

        state.npcs = [

            SirLeopoldTheHedgeHog(16 * 11, 16 * 30),
            QuestGiverJanet(16 * 21, 16 * 20),
            BarKeep(16 * 31, 16 * 10),
            CindyLongHair(16 * 31, 16 * 20),
            Guy(16 * 31, 16 * 28)

        ]






    def update(self, state: "GameState"):
        # state.player.canMove = False
        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()

        self.timer += 1 / 60

        # Start moving the player after 2 seconds
        if self.timer >= 2 and not self.player_moved:
            print("Starting controlled movement")
            self.movement_start_time = self.timer  # Store the time when the player starts moving
            self.player_moved = True  # Indicate that the player has started moving

        # If the player has started moving, check the time elapsed since the movement started
        if self.player_moved:
            movement_duration = self.timer - self.movement_start_time

            # If it's been less than 2 seconds since the player started moving, keep moving
            if movement_duration < 2:
                state.player.velocity.y = -2  # Move up by setting a negative velocity
            else:
                # 2 seconds have passed, stop the movement
                state.player.velocity.y = 0
                print("2 seconds have passed, stopping movement")







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
