import pygame
import pytmx
import time  # Import the time module

from constants import PLAYER_OFFSET, BLUEBLACK
from cut_scene_manager.cut_scene_movement import CutSceneMovement
from entity.gui.textbox.npc_text_box import NpcTextBox
from entity.npc.area2.area_2_nugget_screen.erika_chicken_girl import ErikaChickenGirl
from entity.npc.battle_screen.Guy import Guy

from entity.npc.chilli_screen.sir_leopold_the_hedgehog import SirLeopoldTheHedgeHog

from entity.npc.rest_screen.bar_keep import BarKeep

from entity.npc.rest_screen.quest_giver_janet import QuestGiverJanet

from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.player.player import Player
from game_constants.treasure import Treasure
from screen.examples.screen import Screen
from physics.rectangle import Rectangle
from concurrent.futures import ThreadPoolExecutor



class Area2BarCutScene1(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/rest_area_2_final_map.tmx")

        move_player_down_flag = False
        self.npcs = [
        ]

        self.timer_paused = False
        self.fixed_time = None
        self.initial_player_y = None

        self.cut_scene_movement = CutSceneMovement()
        self.timer_start = time.time()  # Initialize the timer at the start of the screen

        self.timer = 0  # Timer to track time since the screen started
        self.player_moved = False  # Flag to track if the player has been moved
        self.move_distance = 30  # Distance to move the player during the cutscene
        # Initialize the clock

        self.music_file =  "/Users/stevenhalla/code/casino_hell/assets/music/relax_screen.mp3"

        self.display_message1 = False  # Flag to track if the message should be displayed
        self.display_message2 = False  # Flag to track if the message should be displayed
        self.timer_start = None  # To store the start time of the timer
        self.timer_duration = 2


        self.cut_scene_1_messages = {
            "message_1": NpcTextBox(
                [
                    "Erika: Hello Hero its so good to see you finally, I've been wanting to chat with you for a while now",
                    "Hero: Oh yeah? Can you tell me whats up.",
                    "Sir Leopold: I hope this is worth the 2000 coins, hero had to work hard for every coin",
                    "Erika: Oh yes, this is very much worth it. I need you to go to the rib demon maze and get me their special treasure",
                    "Hero: Wel that sounds easy enough",
                    "SIr leopold: Yeah, a little too easy, what's the catch?",
                    "Erika: Catch....well the entire place is filled with a poison mist, I would go there myself,but my tiny wittle chicky lungs wouldn't be able to handle it?",
                    "Erika: I  need you to fetch the super secret rib demon ultimate rib sauce",
                    "Hero: Sounds like I'm risking my life for something thats not that important",
                    "Erika: Oh your not risking your life, but your soul will be bound to 'the wall' if you fail and they'll eat your ribs for all eternity if you perish",
                    "It may  sound like your risking your immortal soul for something small, but it's really really important to get that recipe",
                    "Sir Leopold: Hero i don't think you should do it, sounds too dangerous",
                    "Hero: Oh come now have more faith in me, Im feeling lucky little buddy.",
                    "Erika: oh very nice hero, I knew it in my chicken nuggy heart you would help,I'll give you some advice on how to complete your task:",
                    "There are 3 floors to the maze, the first of which has blind and deaf demons, but they can detect changes in air density in a small radius",
                    "There are barrels you can climb inside of that will protect you",
                    "Erika: The second floor will have switches that you'll need to press in a certain order",
                    "Sir Leopold:What order does he need to press them in?",
                    "Erika: The switches that are the farthest from each other....just be aware of the stalker demon, you can slow him down using the blue tiles",
                    "Erika: If you mess up the order you'll have to start over",
                    "Hero: How do you know all of this if you've never been there before?",
                    "Erika: How long do you think I've been here? Not like I dont have anything better to do than get info?",
                    "On the 3rd and final level there are 3 switches to press, do so and you'll disable the stalker demon?",
                    "Erika: Good luck Hero, and the other one will need to stay out, or he'll die",
                    "Sir leopold: My name is Sir Leopold",
                    "Erika: I already forgot your name...I'll call you hedgy....good luck hero! And before I forget here's the key",





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

        self.current_movement_index = 0
        self.movement_sequence = [
            ('move_right', 1),
            ('move_up', 1)
        ]
        self.event_counter = 0

        self.game_state = "step_3"
        self.state_start_time = None
        self.state_duration = 1  # Duration for each state

    def start(self, state: "GameState"):
        player_start_x = 16 * 130  # Desired X coordinate
        player_start_y = 16 * 8  # Desired Y coordinate
        state.player.setPosition(player_start_x, player_start_y)


        state.restScreen.barscene1 = True
        state.restScreen.bar_keeper_talking = False



        super().start(state)

        # self.timer_start = time.time()  # Initialize the timer at the start of the screen

        self.timer_start = time.time()  # Initialize the timer at the start of the screen

        # Check if a player instance already exists
        # times 16


        state.npcs = [
            SirLeopoldTheHedgeHog(16 * 125, 16 * 8),
            ErikaChickenGirl(16 * 135, 16 * 8),
            BarKeep(16 * 130, 16 * 4)


        ]

    def update(self, state: "GameState"):

        current_time = time.time()




        if self.game_state == "step_3":

            print(f"STEP 3")

            self.current_message = self.cut_scene_1_messages["message_1"]
            self.current_message.update(state)
            if self.current_message.is_finished() and state.controller.isTPressed:
                print("hi")
                self.game_state = "step_4"
                Treasure.add_quest_to_player(state.player, Treasure.RIB_DEMON_KEY)

                state.controller.isTPressed = False
                state.player.canMove = True
                state.player.food = 0

                state.currentScreen = state.area2RestScreen
                state.area2RestScreen.start(state)

        # state.player.canMove = False
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

        if self.game_state == "step_3":
            self.cut_scene_1_messages["message_1"].draw(state)

        state.obstacle.draw(state)

        state.player.draw(state)

        # Update the display
        pygame.display.update()
