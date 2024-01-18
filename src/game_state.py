import pygame

from entity.npc.start_screen.cindy_long_hair import CindyLongHair
from entity.npc.rest_screen.quest_giver_janet import QuestGiverJanet
from screen.black_jack_rumble_bill_screen import BlackJackRumbleBillScreen
from screen.black_jack_screen import BlackJackScreen
from screen.black_jack_thomas_screen import BlackJackThomasScreen
from screen.coin_flip_fred_screen import CoinFlipFredScreen
from screen.coin_flip_sandy_screen import CoinFlipSandyScreen
from screen.coin_flip_ted_screen import CoinFlipTedScreen
from constants import WINDOWS_SIZE, GREEN, BLUE
from controller import Controller
from entity.obstacle.obstacle import Obstacle
from screen.gambling_area_screen import GamblingAreaScreen
from screen.main_screen import MainScreen
from screen.opossum_in_a_can_nelly_screen import OpossumInACanNellyScreen
from screen.opossum_in_a_can_screen import OpossumInACanScreen
from entity.player.player import Player
from physics.vector import Vector
from screen.rest_screen import RestScreen
from screen.start_screen import StartScreen


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
        self.player: Player = Player(16 * 5, 16 * 11)
        self.cindy_long_hair: CindyLongHair = CindyLongHair(0,0)
        self.quest_giver_janet: QuestGiverJanet = QuestGiverJanet(0,0)
        self.npcs = []  # load npcs based on which screen (do not do here, but do in map load function (screen start())
        self.demons = []  # load npcs based on which screen (do not do here, but do in map load function (screen start())
        self.treasurechests = []
        # self.npcs = [CoinFlipFred(175, 138), SalleyOpossum(65, 28), ChiliWilley(311, 28)]
        self.obstacle = Obstacle(444, 999)

        self.isRunning: bool = True
        self.isPaused: bool = False
        self.delta: float = 0.0
        self.camera = Vector(0.0, 0.0)

        self.mainScreen = MainScreen()
        self.restScreen = RestScreen()
        self.gamblingAreaScreen = GamblingAreaScreen()
        # self.restScreen = RestScreen()
        # self.hedgeMazeScreen = HedgeMazeScreen()
        # self.bossScreen = BossScreen()
        self.startScreen = StartScreen()

        self.coinFlipTedScreen = CoinFlipTedScreen()
        self.coinFlipFredScreen = CoinFlipFredScreen()
        self.coinFlipSandyScreen = CoinFlipSandyScreen()

        self.opossumInACanScreen = OpossumInACanScreen()
        self.opossumInACanNellyScreen = OpossumInACanNellyScreen()

        self.blackJackScreen = BlackJackScreen()
        self.blackJackThomasScreen = BlackJackThomasScreen()
        self.blackJackRumbleBillScreen = BlackJackRumbleBillScreen()

        self.currentScreen = self.gamblingAreaScreen  # assign a value to currentScreen here
