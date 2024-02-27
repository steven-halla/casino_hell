import pygame
import pytmx

from constants import PLAYER_OFFSET, BLUEBLACK
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
from entity.treasurechests.powerpotion import PowerPotion
from screen.examples.screen import Screen
from physics.rectangle import Rectangle



class WinScreen(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.font = pygame.font.Font(None, 36)
        self.music_file = "/Users/stevenhalla/code/casino_hell/assets/music/relax_screen.mp3"

        self.music_volume = 0.5  # Adjust as needed
        self.initialize_music()
        self.clock = pygame.time.Clock()  # Initialize the clock








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
        if state.musicOn == True:
            self.initialize_music()
        # self.initialize_music()
        super().start(state)
        state.npcs.clear()





    def update(self, state: "GameState"):

        controller = state.controller
        player = state.player
        controller.update()

        if controller.isExitPressed is True:
            state.isRunning = False


        player.update(state)





    def draw(self, state: "GameState"):

        state.DISPLAY.fill(BLUEBLACK)
        state.DISPLAY.blit(self.font.render(f"You beat the evil demon, but there is more to come.", True,
                                                (255, 255, 255)), (70, 460))

        pygame.display.update()
