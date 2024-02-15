import pygame
import json


from entity.demon.demon1 import Demon1
from entity.npc.rest_screen.shop_keeper import ShopKeeper
from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.npc.rest_screen.quest_giver_janet import QuestGiverJanet
from screen.floor1.battle_screens.black_jack_jared_screen import BlackJackJaredScreen
from screen.floor1.battle_screens.black_jack_rumble_bill_screen import BlackJackRumbleBillScreen
from screen.examples.black_jack_screen import BlackJackScreen
from screen.floor1.battle_screens.black_jack_thomas_screen import BlackJackThomasScreen
from screen.floor1.battle_screens.coin_flip_ted_screen import CoinFlipTedScreen
from screen.floor1.battle_screens.demon_boss_screen import DemonBossScreen
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
from screen.examples.main_screen import MainScreen
from screen.floor1.battle_screens.opossumInACanIchi import OpossumInACanIchiScreen
from screen.floor1.battle_screens.opossum_in_a_can_nelly_screen import OpossumInACanNellyScreen
from screen.floor1.battle_screens.opossum_in_a_can_sally_screen import OpossumInACanSallyScreen
from screen.examples.opossum_in_a_can_screen import OpossumInACanScreen
from entity.player.player import Player
from physics.vector import Vector
from screen.floor1.map_screens.rest_screen import RestScreen
from screen.floor1.map_screens.start_load_screen import StartLoadScreen
from screen.floor1.map_screens.start_screen import StartScreen


class GameState:
    def __init__(self):

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

        self.entryPoint = None


        self.obstacle = Obstacle(444, 999)
        self.isRunning: bool = True
        self.isPaused: bool = False
        self.delta: float = 0.0
        self.camera = Vector(0.0, 0.0)
        self.sir_leopold_companion = False

        self.startScreen = StartScreen()
        self.chilliScreen = ChilliScreen()
        self.mainScreen = MainScreen()
        self.restScreen = RestScreen()
        self.gamblingAreaScreen = GamblingAreaScreen()
        self.hotelRoomScreen = HotelRoomScreen()
        self.bossScreen = BossScreen()
        self.hedgeMazeScreen = HedgeMazeScreen()

        self.barCutScene1 = BarCutScene1Screen()
        self.barCutScene2 = BarCutScene2Screen()
        self.gameOverScreen = GameOverScreen()

        self.coinFlipScreen = CoinFlipScreen()
        self.coinFlipTedScreen = CoinFlipTedScreen()
        self.coinFlipFredScreen = CoinFlipFredScreen()
        self.coinFlipSandyScreen = CoinFlipSandyScreen()

        self.opossumInACanScreen = OpossumInACanScreen()
        self.opossumInACanNellyScreen = OpossumInACanNellyScreen()
        self.opossumInACanSallyScreen = OpossumInACanSallyScreen()
        self.opossumInACanIchiScreen = OpossumInACanIchiScreen()

        self.blackJackScreen = BlackJackScreen()
        self.blackJackThomasScreen = BlackJackThomasScreen()
        self.blackJackRumbleBillScreen = BlackJackRumbleBillScreen()
        self.blackJackJaredScreen = BlackJackJaredScreen()
        self.blackJackDemonBossScreen = DemonBossScreen()

        self.startLoadScreen = StartLoadScreen()


        self.currentScreen = self.blackJackDemonBossScreen


        self.start_new_game_entry_point = False
        self.rest_area_to_start_area_entry_point = False


    def save_game(self, player, state: "GameState"):
        # Convert player stats to dictionary
        player_data = player.to_dict(state)

        # Convert dictionary to JSON string
        player_json = json.dumps(player_data, indent=4)

        # Define the file path
        file_path = '/Users/stevenhalla/code/casino_hell/assets/save_data.json'

        # Write JSON string to a file at the specified path
        with open(file_path, 'w') as file:
            file.write(player_json)


        # assign a value to currentScreen here
