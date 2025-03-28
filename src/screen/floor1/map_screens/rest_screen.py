import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
from entity.demon.demon1 import Demon1
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



class RestScreen(Screen):

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
        self.rest_screen_npc_janet_talk_first_five_hundred = False
        self.rest_screen_npc_janet_quest_2_counter = False
        self.rest_screen_npc_janet_quest_3_counter = False
        self.rest_screen_npc_janet_find_hog = False

        self.barscene1 = False
        self.barscene2 = False

        self.clock = pygame.time.Clock()  # Initialize the clock



        self.nurgle_turned_in = False

        self.bar_keeper_talking = False



        self.npc_janet_textbox2 = False
        self.npc_janet_textbox3 = False
        self.npc_janet_textbox4 = False
        self.npc_janet_textbox5 = False
        self.npc_janet_textbox6 = False

        self.nurgle_the_hedge_hog = True

        self.music_file =  "./assets/music/relax_screen.mp3"

        self.music_volume = 0.5  # Adjust as needed
        self.initialize_music()
        self.inn_badge_recieved_tracker = False
        self.nurgle_found = False


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

        # receiving
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

        # Add the appropriate NPC based on the player's body value

        state.treasurechests = [
        ]

        # if state.player.perception > 0 and self.powerpotiongotten == False and:
        #     state.treasurechests.append(PowerPotion(16 * 27, 14 * 10))

        # if state.gamblingAreaScreen.nurgle_the_hedge_hog == True:
        #     print("is there a nurgle here?")
        #     state.npcs.append(Nurgle(16 * 25, 16 * 22))

        # Add other NPCs to the state.npcs list
        state.npcs.extend([
            DoctorOpossum(16 * 26, 16 * 20),
            InnKeeper(16 * 101, 16 * 33),
            # JustinNoFruit(16 * 10, 16 * 18),
            JustinNoFruit(16 * 52, 16 * 13),
            # EvilCat(16 * 54, 16 * 13),
            # QuestGiverJanet(16 * 10, 16 * 26),
            ChiliPitTeleporter(16 * 15, 16 * 49),

            SufferingSuzy(16 * 26, 16 * 26),
            WallyGuide(16 * 75, 16 * 46),
            StartScreenTeleporter(16 * 17, 16 * 0),
            NewTeleporter(16 * 95, 16 * 0),
            BossTeleporter(16 * 64, 16 * 49),
        ])
        #
        # if state.quest_giver_janet.find_hog:
        #     state.npcs.append(Nurgle(16 * 24, 16 * 34))

        state.demons = [
            # Demon1(16 * 5, 16 * 5),
            # Demon2(16 * 55, 16 * 13),
            # Demon3(16 * 55, 16 * 23),
            # Demon4(16 * 55, 16 * 33),
        ]

    def update(self, state: "GameState"):
        # timer = self.clock.tick(60)
        self.clock.tick(60)
        # print("Your rest screen game clock is: " + str(timer))


        if state.player.perception > 0 and self.powerpotiongotten == False and state.player.hasRabies == False:
            state.treasurechests.append(PowerPotion(16 * 27, 14 * 10))

        if state.player.body > 0:
            state.treasurechests = [item for item in state.treasurechests if not isinstance(item, PowerPotion)]




        # if self.chili_pit_flag == True:
        #     state.npcs.append(ChiliPitTeleporter(16 * 30, 16 * 18))
        # i dont think npc and demons getting updated
        # print(state.quest_giver_janet.find_hog)
        # print(state.quest_giver_janet.quest2counter)

        if state.player.body > 0 and state.player.hasRabies == False:
            # Check if an instance of BarKeep already exists
            if not any(isinstance(npc, BarKeep) for npc in state.npcs):
                state.npcs.append(BarKeep(16 * 36, 16 * 16))
            # Ensure no instance of BarKeepLowBody is present
            state.npcs = [npc for npc in state.npcs if not isinstance(npc, BarKeepLowBody)]
        else:
            # Check if an instance of BarKeepLowBody already exists
            if not any(isinstance(npc, BarKeepLowBody) for npc in state.npcs):
                state.npcs.append(BarKeepLowBody(16 * 36, 16 * 16))
            # Ensure no instance of BarKeep is present
            state.npcs = [npc for npc in state.npcs if not isinstance(npc, BarKeep)]

        controller = state.controller
        player = state.player
        obstacle = state.obstacle
        controller.update()
        if state.player.perception > 0:
            shop_keeper_instance = state.shop_keeper

        # Now, you can interact with the ShopKeeper instance
        # For example, calling its update method:
            shop_keeper_instance.update(state)

        janet_keeper_instance = state.quest_giver_janet

        # Now, you can interact with the ShopKeeper instance
        # For example, calling its update method:
        janet_keeper_instance.update(state)

        #the below speeds up text speech
        # for npc in state.npcs:
        #     npc.update(state)
        #     if isinstance(npc, Nurgle) and npc.to_be_deleted:
        #         state.npcs.remove(npc)

        for npc in state.npcs:
            npc.update(state)
            if isinstance(npc, BarKeepLowBody) and state.player.body > 0:
                state.npcs.remove(npc)


        # Game Update Loop
        if state.player.body < 1:
            for chest in state.treasurechests:
                chest.update(state)



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

        # for npc in state.npcs:
        #     if isinstance(npc, ShopKeeper):
        #         npc.textbox.draw(state)

        for demon in state.demons:
            demon.draw(state)

        if state.player.body < 1 and state.player.perception > 0:
            for treasurechests in state.treasurechests:
                treasurechests.draw(state)

        state.obstacle.draw(state)

        state.player.draw(state)

        if state.player.perception > 0:
            shop_keeper_instance = state.shop_keeper
            shop_keeper_instance.draw(state)

        janet_instance = state.quest_giver_janet
        janet_instance.draw(state)

        if state.controller.isPPressed == True:

            state.player.draw_player_stats(state)

            if state.controller.isBPressed == True:
                if state.controller.isPPressed:
                    state.controller.isPPressed = False
                    return

        # Update the display
        pygame.display.update()
