import pygame

from entity.npc.cindy_long_hair import CindyLongHair
from screen.black_jack_screen import BlackJackScreen
from screen.coin_flip_fred_screen import CoinFlipFredScreen
from screen.coin_flip_sandy_screen import CoinFlipSandyScreen
from screen.coin_flip_ted_screen import CoinFlipTedScreen
from constants import WINDOWS_SIZE, GREEN, BLUE
from controller import Controller
from screen.dice_game_screen import DiceGameScreen
from entity.obstacle.obstacle import Obstacle
from screen.main_screen import MainScreen
from screen.opossum_in_a_can_nelly_screen import OpossumInACanNellyScreen
from screen.opossum_in_a_can_screen import OpossumInACanScreen
from entity.player.player import Player
from physics.vector import Vector



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
        self.player: Player = Player(16 * 20, 16 * 34)
        self.cindy_long_hair: CindyLongHair = CindyLongHair(0,0)
        self.npcs = []  # load npcs based on which screen (do not do here, but do in map load function (screen start())
        self.demons = []  # load npcs based on which screen (do not do here, but do in map load function (screen start())
        self.treasurechests = []
        # self.npcs = [CoinFlipFred(175, 138), SalleyOpossum(65, 28), ChiliWilley(311, 28)]
        self.obstacle = Obstacle(22, 622)

        self.isRunning: bool = True
        self.isPaused: bool = False
        self.delta: float = 0.0
        self.camera = Vector(0.0, 0.0)

        self.mainScreen = MainScreen()
        # self.restScreen = RestScreen()
        # self.hedgeMazeScreen = HedgeMazeScreen()
        # self.bossScreen = BossScreen()

        self.coinFlipTedScreen = CoinFlipTedScreen()
        self.coinFlipSandyScreen = CoinFlipSandyScreen()
        self.opossumInACanScreen = OpossumInACanScreen()
        self.blackJackScreen = BlackJackScreen()

        self.currentScreen = self.opossumInACanScreen  # assign a value to currentScreen here
