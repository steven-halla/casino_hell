import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.npc.hedge_maze_screen.hedgehog1 import HedgeHog1
from entity.npc.hedge_maze_screen.hedgehog2 import HedgeHog2
from entity.npc.hedge_maze_screen.hedgehog3 import HedgeHog3
from entity.npc.hedge_maze_screen.hedgehog4 import HedgeHog4
from entity.npc.rest_screen.bar_keep import BarKeep
from entity.npc.rest_screen.bar_keep_low_body import BarKeepLowBody
from entity.npc.rest_screen.doctor_opossum import DoctorOpossum
from entity.npc.rest_screen.hedgeMazeTeleporter import HedgeMazeScreenTeleporter
from entity.npc.rest_screen.inn_keeper import InnKeeper
from entity.npc.rest_screen.justin_no_fruit import JustinNoFruit
from entity.npc.rest_screen.new_teleporter import NewTeleporter
from entity.npc.rest_screen.quest_giver_janet import QuestGiverJanet

from entity.npc.rest_screen.start_screen_teleporter import StartScreenTeleporter
from entity.npc.rest_screen.suffering_suzy import SufferingSuzy
from entity.npc.rest_screen.wally_guide import WallyGuide
from entity.npc.start_screen.inn_guard import InnGuard
from entity.npc.nurgle import Nurgle
from entity.player.player import Player
from screen.examples.screen import Screen
from physics.rectangle import Rectangle



class RestScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
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

    def start(self, state: "GameState"):
        super().start(state)
        state.npcs.clear()

        # Check if a player instance already exists
        if not hasattr(state, 'player') or state.player is None:
            player_start_x = 300
            player_start_y = 200
            state.player = Player(player_start_x, player_start_y)

        state.treasurechests = [

            # WaterBottle(16 * 36, 16 * 10),

        ]
        # Check the value of state.player.body

        state.npcs = []
        if state.player.body > 0:
            state.npcs.append(BarKeep(16 * 36, 16 * 18))
        elif state.player.body == 0:
            state.npcs.append(BarKeepLowBody(16 * 36, 16 * 18))

        # if state.gamblingAreaScreen.nurgle_the_hedge_hog == True:
        #     print("is there a nurgle here?")
        #     state.npcs.append(Nurgle(16 * 25, 16 * 22))

        # Add other NPCs to the state.npcs list
        state.npcs.extend([
            DoctorOpossum(16 * 26, 16 * 18),
            InnKeeper(16 * 18, 16 * 18),
            JustinNoFruit(16 * 10, 16 * 18),
            # QuestGiverJanet(16 * 10, 16 * 26),

            SufferingSuzy(16 * 26, 16 * 26),
            WallyGuide(16 * 34, 16 * 26),
            StartScreenTeleporter(16 * 5, 16 * 25),
            NewTeleporter(16 * 15, 16 * 35),
            HedgeMazeScreenTeleporter(16 * 6, 16 * 35),
        ])
        #
        # if state.quest_giver_janet.find_hog:
        #     state.npcs.append(Nurgle(16 * 24, 16 * 34))

        state.demons = [
            # Demon1(16 * 55, 16 * 3),
            # Demon2(16 * 55, 16 * 13),
            # Demon3(16 * 55, 16 * 23),
            # Demon4(16 * 55, 16 * 33),
        ]

    def update(self, state: "GameState"):
        # i dont think npc and demons getting updated
        # print(state.quest_giver_janet.find_hog)
        # print(state.quest_giver_janet.quest2counter)


        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()
        shop_keeper_instance = state.shop_keeper

        # Now, you can interact with the ShopKeeper instance
        # For example, calling its update method:
        shop_keeper_instance.update(state)

        janet_keeper_instance = state.quest_giver_janet

        # Now, you can interact with the ShopKeeper instance
        # For example, calling its update method:
        janet_keeper_instance.update(state)


        for npc in state.npcs:
            npc.update(state)
            if isinstance(npc, Nurgle) and npc.to_be_deleted:
                state.npcs.remove(npc)



        # Assuming you have your hedgehog instances named like HedgeHog1, HedgeHog2, etc.
        # hedgehogs = [HedgeHog1(), HedgeHog2(), HedgeHog3(), HedgeHog4()]


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

        shop_keeper_instance = state.shop_keeper
        shop_keeper_instance.draw(state)

        janet_instance = state.quest_giver_janet
        janet_instance.draw(state)

        # Update the display
        pygame.display.update()
