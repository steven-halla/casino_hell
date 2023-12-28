import pygame

from black_jack_screen import BlackJackScreen
from coin_flip_ted_screen import CoinFlipTedScreen
from constants import WINDOWS_SIZE, GREEN, BLUE
from controller import Controller
from dice_game_screen import DiceGameScreen
from obstacle import Obstacle
from main_screen import MainScreen
from opossum_in_a_can_nelly_screen import OpossumInACanNellyScreen
from opossum_in_a_can_screen import OpossumInACanScreen
from player import Player
from vector import Vector


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
        self.npcs = []  # load npcs based on which screen (do not do here, but do in map load function (screen start())
        self.demons = []  # load npcs based on which screen (do not do here, but do in map load function (screen start())
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
        self.opossumInACanScreen = OpossumInACanScreen()
        self.opossumInACanNellyScreen = OpossumInACanNellyScreen()
        self.blackJackScreen = BlackJackScreen()
        self.diceGameScreen = DiceGameScreen()

        self.currentScreen = self.mainScreen  # assign a value to currentScreen here
