import pygame
import pytmx

from entity.demon.demon1 import Demon1
from entity.npc.FlippingSandy import FlippingSandy
from entity.npc.bapping_mike import BappingMike
from entity.npc.bar_keep import BarKeep
from entity.npc.bobby_bibs import BobbyBibs
from entity.npc.brutal_patrick import BrutalPatrick
from entity.npc.chilly_billy import ChillyBilly
from entity.npc.cindy_long_hair import CindyLongHair
from constants import PLAYER_OFFSET, BLUEBLACK, TILE_SIZE
from entity.npc.coin_flip_fred import CoinFlipFred
from entity.npc.flippin_ted import FlippinTed
from entity.npc.hedgehog1 import HedgeHog1
from entity.npc.hedgehog2 import HedgeHog2
from entity.npc.hedgehog3 import HedgeHog3
from entity.npc.hedgehog4 import HedgeHog4
from entity.npc.hungry_patrick import HungryPatrick
from entity.npc.inn_guard import InnGuard
from entity.npc.inn_keeper import InnKeeper
from entity.npc.nelly_opossum import NellyOpossum
from entity.npc.nurgle import Nurgle
from entity.npc.quest_giver_janet import QuestGiverJanet
from entity.npc.shop_keeper import ShopKeeper
from entity.npc.suffering_suzy import SufferingSuzy
from entity.player.player import Player
from entity.treasurechests.waterbottle import WaterBottle
from screen.screen import Screen
from entity.npc.jacky_banana import JackyBanana
from entity.npc.justin_no_fruit import JustinNoFruit
from entity.npc.nicky_hints import NickyHints
from physics.rectangle import Rectangle
from entity.npc.rumble_bill import RumbleBill
from entity.npc.sally_opossum import SallyOpossum
from entity.npc.sleepy_ned import SleepyNed
from entity.npc.wally_guide import WallyGuide



class MainScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map = pytmx.load_pygame("./assets/map/casinomaingame4.tmx")
        self.y_up_move = False
        self.y_down_move = False
        self.x_left_move = False
        self.x_right_move = False
        self.player = Player(400, 200)
        self.hedge_hog_counter = 0
        move_player_down_flag = False

    def start(self, state: "GameState"):
        super().start(state)

        # Check if a player instance already exists
        if not hasattr(state, 'player') or state.player is None:
            player_start_x = 300
            player_start_y = 200
            state.player = Player(player_start_x, player_start_y)

        state.treasurechests = [

            WaterBottle(16 * 36, 16 * 10),

        ]

        # state.npcs = []
        state.npcs = [
            # make sure to seperate by a factor of 8 for y
            #x, y
            # InnGuard(16 * 36, 16 * 2),
            # BappingMike(16 * 36, 16 * 10),
            # BarKeep(16 * 36, 16 * 18),
            # InnKeeper(16 * 36, 16 * 26),


            # BobbyBibs(16 * 2, 16 * 2),
            # BrutalPatrick(16 * 2, 16 * 10),
            # ChillyBilly(16 * 2, 16 * 18),
            #  CindyLongHair(16 * 2, 16 * 26),
             # HungryPatrick(16 * 2, 16 * 34),
            # JackyBanana(16 * 10, 16 * 2),
            # JustinNoFruit(16 * 10, 16 * 10),
            # NickyHints(16 * 10, 16 * 18),
            # QuestGiverJanet(16 * 10, 16 * 26),
            # RumbleBill(16 * 18, 16 * 2),
            # SallyOpossum(16 * 18, 16 * 10),
            # ShopKeeper(16 * 18, 16 * 18),
            # SleepyNed(16 * 18, 16 * 26),
            # SufferingSuzy(16 * 26, 16 * 2),
            WallyGuide(16 * 26, 16 * 10),
            #
            # CoinFlipFred(16 * 28, 16 * 36),
            FlippinTed(16 * 20, 16 * 36),
            FlippingSandy(16 * 28, 16 * 36),
            # NellyOpossum(16 * 12, 16 * 36),
            # Nurgle(16 * 24, 16 * 34)
            HedgeHog1(16 * 24, 16 * 34),
            HedgeHog2(16 * 32, 16 * 34),
            HedgeHog3(16 * 24, 16 * 20),
            HedgeHog4(16 * 24, 16 * 15),


                      ]

        state.demons = [
            Demon1(16 * 32, 16 * 10)

        ]

    def update(self, state: "GameState"):
        # i dont think npc and demons getting updated



        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()
        for npc in state.npcs:
            npc.update(state)
            if isinstance(npc, Nurgle) and npc.to_be_deleted:
                state.npcs.remove(npc)

        # Assuming you have your hedgehog instances named like HedgeHog1, HedgeHog2, etc.
        # hedgehogs = [HedgeHog1(), HedgeHog2(), HedgeHog3(), HedgeHog4()]

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

        for demon in state.demons:
            demon.draw(state)

        for treasurechests in state.treasurechests:
            treasurechests.draw(state)

        state.obstacle.draw(state)

        state.player.draw(state)

        # Update the display
        pygame.display.update()
