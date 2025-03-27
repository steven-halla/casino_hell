import pygame
import json




from entity.demon.demon1 import Demon1
from entity.gui.textbox.text_box import TextBox
from entity.npc.rest_screen.shop_keeper import ShopKeeper
from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.npc.rest_screen.quest_giver_janet import QuestGiverJanet
from screen.floor1.battle_screens.black_jack_jared_screen import BlackJackJaredScreen
from screen.floor1.battle_screens.black_jack_rumble_bill_screen import BlackJackRumbleBillScreen
from screen.examples.black_jack_screen import BlackJackScreen
from screen.floor1.battle_screens.black_jack_thomas_screen import BlackJackThomasScreen
from screen.floor1.battle_screens.coin_flip_ted_screen import CoinFlipTedScreen
from screen.floor1.battle_screens.demon_boss_screen import DemonBossScreen
from screen.floor1.battle_screens.opossum_in_a_can_sally_screen import OpossumInACanSallyScreen
from screen.floor1.battle_screens.opossum_in_a_can_nelly_screen import OpossumInACanNellyScreen
from screen.floor1.map_screens.barcutscene1 import BarCutScene1Screen
from screen.floor1.map_screens.barcutscene2 import BarCutScene2Screen
from screen.floor1.map_screens.boss_screen import BossScreen
from screen.floor1.map_screens.chilli_screen import ChilliScreen
from screen.floor1.battle_screens.coin_flip_fred_screen import CoinFlipFredScreen
from screen.floor1.battle_screens.coin_flip_sandy_screen import CoinFlipSandyScreen
from screen.examples.coin_flip_screen import CoinFlipScreen
from constants import WINDOWS_SIZE, GREEN, BLUE
from controller import Controller
from entity.obstacle.obstacle import Obstacle
from screen.floor1.map_screens.gambling_area_screen import GamblingAreaScreen
from screen.floor1.map_screens.game_over_screen import GameOverScreen
from screen.floor1.map_screens.hedge_maze_screen import HedgeMazeScreen
from screen.floor1.map_screens.hotel_room_screen import HotelRoomScreen
from screen.floor1.battle_screens.opossumInACanIchi import OpossumInACanIchiScreen
# from screen.floor1.battle_screens.opossum_in_a_can_nelly_screen import OpossumInACanNellyScreen
# from screen.floor1.battle_screens.opossum_in_a_can_sally_screen import OpossumInACanSallyScreen
# from screen.examples.opossum_in_a_can_screen import OpossumInACanScreen
from entity.player.player import Player
from physics.vector import Vector
from screen.floor1.map_screens.rest_screen import RestScreen
from screen.floor1.map_screens.start_load_screen import StartLoadScreen
from screen.floor1.map_screens.start_screen import StartScreen
from screen.floor1.map_screens.win_screen import WinScreen
from screen.floor2.battle_screens.black_jack_mack_screen import BlackJackMackScreen
from screen.floor2.battle_screens.coin_flip_betty_screen import CoinFlipBettyScreen
from screen.floor2.battle_screens.craps_boss_screen import CrapsBossScreen

from screen.floor2.battle_screens.craps_happy_screen import CrapsHappyScreen
from screen.floor2.battle_screens.hungry_starving_hippos import HungryStarvingHippos
from screen.floor2.battle_screens.hungry_starving_hippos2 import HungryStarvingHippos2
from screen.floor2.battle_screens.opossum_in_a_can_candy_screen import OpossumInACanCandyScreen
from screen.floor2.battle_screens.slots_rib_demon_jack_ripper_screen import SlotsRippaSnappaScreen
from screen.floor2.cut_scenes.area_2_bar_cut_scene_1 import Area2BarCutScene1
from screen.floor2.cut_scenes.area_2_bar_cut_scene_2 import Area2BarCutScene2
from screen.floor2.cut_scenes.area_2_bar_cut_scene_3 import Area2BarCutScene3
from screen.floor2.map_screens.area_2_boss_screen import Area2BossScreen
from screen.floor2.map_screens.area_2_boss_screen_after_reveal import Area2BossAfterRevealScreen
from screen.floor2.map_screens.area_2_gambling_screen import Area2GamblingScreen
from screen.floor2.map_screens.area_2_nugget_screen import Area2NuggetScreen
from screen.floor2.map_screens.area_2_rest_screen import Area2RestScreen
from screen.floor2.map_screens.area_2_rib_demon_maze_screen import Area2RibDemonMazeScreen
from screen.floor2.map_screens.area_2_rib_demon_maze_screen2 import Area2RibDemonMazeScreen2
from screen.floor2.map_screens.area_2_rib_demon_maze_screen3 import Area2RibDemonMazeScreen3
from screen.floor2.map_screens.area_2_start_screen import Area2StartScreen
from screen.floor3.battle_screens.black_jack_albert_screen import BlackJackAlbertScreen
from screen.floor3.battle_screens.coin_flip_dexter_screen import CoinFlipDexterScreen
from screen.floor3.battle_screens.craps_junpon_screen import CrapsJunponScreen
from screen.floor3.battle_screens.dice_fighter_sir_siegfried_screen import DiceFighterSirSiegfriedScreen
from screen.floor3.battle_screens.high_low_diena_screen import HighLowDienaScreen
from screen.floor3.battle_screens.hungry_starving_hippos_hippy_screen import HungryStarvingHipposHippyScreen
from screen.floor3.battle_screens.opossum_in_a_can_billy_bob_screen import OpossumInACanBillyBobScreen


from screen.floor3.battle_screens.slots_brogan_screen import SlotsBroganScreen
from screen.floor3.map_screens.area_3_rest_screen import Area3RestScreen
from screen.menu_screen.equipment_screen import EquipmentScreen


class GameState:
    def __init__(self):
        self.game_over_message = TextBox([""], (65, 460, 700, 130), 36, 500)


        # shared pygame constructs
        self.DISPLAY: pygame.Surface = pygame.display.set_mode(WINDOWS_SIZE)
        self.FONT = pygame.font.Font('freesansbold.ttf', 24)


        # Use in NPC only TODO remove
        self.TEXT_SURFACE = self.FONT.render('Casino', True, GREEN, BLUE)
        self.TEXT_SURFACE_RECT = self.TEXT_SURFACE.get_rect()

        # core game state
        self.controller: Controller = Controller()

        self.player: Player = Player(16 * 555, 16 * 22)
        self.demon_left: Demon1 = Demon1(0,0)
        self.cindy_long_hair: CindyLongHair = CindyLongHair(0,0)
        self.quest_giver_janet: QuestGiverJanet = QuestGiverJanet(16 * 45, 16 * 16)
        self.shop_keeper: ShopKeeper = ShopKeeper(16 * 71, 16 * 7)
        self.npcs = []
        self.demons = []
        self.treasurechests = []
        self.musicOn = False

        self.entryPoint = None


        self.obstacle = Obstacle(55555, 0)
        self.isRunning: bool = True
        self.isPaused: bool = False
        self.delta: float = 0.0
        self.camera = Vector(0.0, 0.0)
        self.sir_leopold_companion = False

        self.startLoadScreen = StartLoadScreen()
        self.startScreen = StartScreen()

        self.chilliScreen = ChilliScreen()
        # self.mainScreen = MainScreen()


        self.restScreen = RestScreen()
        self.gamblingAreaScreen = GamblingAreaScreen()
        self.hotelRoomScreen = HotelRoomScreen()
        self.bossScreen = BossScreen()
        self.hedgeMazeScreen = HedgeMazeScreen()
        #
        self.barCutScene1 = BarCutScene1Screen()
        self.barCutScene2 = BarCutScene2Screen()
        self.gameOverScreen = GameOverScreen()
        self.winGameScreen = WinScreen()

        self.coinFlipScreen = CoinFlipScreen()
        self.coinFlipTedScreen = CoinFlipTedScreen()
        self.coinFlipFredScreen = CoinFlipFredScreen()
        self.coinFlipSandyScreen = CoinFlipSandyScreen()

        # self.opossumInACanScreen = OpossumInACanScreen()
        self.opossumInACanNellyScreen = OpossumInACanNellyScreen()
        self.opossumInACanSallyScreen = OpossumInACanSallyScreen()
        self.opossumInACanIchiScreen = OpossumInACanIchiScreen()

        self.blackJackScreen = BlackJackScreen()
        self.blackJackThomasScreen = BlackJackThomasScreen()
        self.blackJackRumbleBillScreen = BlackJackRumbleBillScreen()
        self.blackJackJaredScreen = BlackJackJaredScreen()
        self.blackJackDemonBossScreen = DemonBossScreen()

# below are the screen for player menu
        self.equipmentScreen = EquipmentScreen()

# level 2 area below
        self.area2StartScreen = Area2StartScreen()
        self.area2RestScreen = Area2RestScreen()
        self.area3RestScreen = Area3RestScreen()
        self.area2GamblingScreen = Area2GamblingScreen()
        self.area2NuggetScreen = Area2NuggetScreen()
        self.area2RibDemonMazeScreen = Area2RibDemonMazeScreen()
        self.area2RibDemonMazeScreen2 = Area2RibDemonMazeScreen2()
        self.area2RibDemonMazeScreen3 = Area2RibDemonMazeScreen3()
        self.area2BossScreen = Area2BossScreen()
        self.area2BossAfterRevealScreen = Area2BossAfterRevealScreen()



        self.slotsRippaSnappaScreen = SlotsRippaSnappaScreen()
        self.hungryStarvingHippos = HungryStarvingHippos()
        self.hungryStarvingHippos2 = HungryStarvingHippos2()
        self.crapsHappyScreen = CrapsHappyScreen()
        self.crapsBossScreen = CrapsBossScreen()
        self.coinFlipBettyScreen = CoinFlipBettyScreen()
        self.blackJackMackScreen = BlackJackMackScreen()
        self.opossumInACanCandyScreen = OpossumInACanCandyScreen()

        self.area2BarCutScene1 = Area2BarCutScene1()
        self.area2BarCutScene2 = Area2BarCutScene2()
        self.area2BarCutScene3 = Area2BarCutScene3()








        self.start_new_game_entry_point = False

        self.gambling_area_to_rest_area_entry_point = False
        self.start_area_to_rest_area_entry_point = False
        self.chili_area_to_rest_area_entry_point = False
        self.maze_area_to_chili_area_entry_point = False
        self.chili_area_to_maze_area_entry_point = False

        self.rest_area_to_boss_area_entry_point = False
        self.rest_area_to_start_area_entry_point = False
        self.rest_area_to_gambling_area_entry_point = False
        self.rest_area_to_chili_area_entry_point = False



        self.area_2_gambling_area_to_rest_point = False
        self.area_2_nugget_area_to_rest_point = False



        self.area_2_rest_area_to_nugget_point = False
        self.area_2_rest_area_to_gambling_point = False
        self.area_2_rest_area_to_rib_demon_maze_point = False
        self.area_2_rest_area_to_rib_demon_maze_point2 = False
        self.area_2_rest_area_to_rib_demon_maze_point3 = False
        self.area_2_rest_area_to_boss_point = False


#-----------------area 3 is beloew-----------------------#
        self.crapsJunponScreen = CrapsJunponScreen()
        self.blackJackAlbertScreen = BlackJackAlbertScreen()
        self.coinFlipDexterScreen = CoinFlipDexterScreen()
        self.opossumInACanBillyBobScreen = OpossumInACanBillyBobScreen()
        self.slotsBroganScreen = SlotsBroganScreen()
        self.diceFighterSirSiegfriedScreen = DiceFighterSirSiegfriedScreen()
        self.highLowDienaScreen = HighLowDienaScreen()
        self.hungryStarvingHipposHippyScreen = HungryStarvingHipposHippyScreen()









        # self.currentScreen = self.crapsBossScreen
        # the below is the default of what i need
        # self.currentScreen = self.startLoadScreen

        self.currentScreen = self.startLoadScreen






    def save_game(self, player, state: "GameState"):
        # Convert player stats to dictionary
        player_data = player.to_dict(state)

        # Convert dictionary to JSON string
        player_json = json.dumps(player_data, indent=4)

        # Define the file path
        # TODO '~/.casino_hell/save_data.json'
        file_path = '/Users/stevenhalla/code/casino_hell/assets/save_data.json'

        # Write JSON string to a file at the specified path
        with open(file_path, 'w') as file:
            file.write(player_json)


        # assign a value to currentScreen here
