import pygame
import pytmx
from constants import PLAYER_OFFSET, BLUEBLACK, TILE_SIZE
from entity.npc.area2trash.area_2_rest_screen.alice import Alice
from entity.npc.area2trash.area_2_rest_screen.rib_demon_jack_ripper import RibDemonJackRipper
from entity.player.player import Player
from screen.examples.screen import Screen
from physics.rectangle import Rectangle


class ExampleScreenBASE(Screen):

    def __init__(self):
        super().__init__("Casino MainScreen")
        self.tiled_map: pytmx.TiledMap = pytmx.load_pygame("./assets/map/startscreen1.tmx")
        self.hedge_hog_counter: int = 0
        self.lock_screen: bool = False
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.music_file: str = "./assets/music/town_music.mp3"
        self.music_volume: float = 0.5
        self.initialize_music()
        self.initialClearNPC: bool = False

    def stop_music(self):
        pygame.mixer.music.stop()

    def initialize_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def start(self, state: "GameState"):
        print("Hi")
        state.npcs = []

        state.npcs =[
            RibDemonJackRipper(16 * 18, 16 * 22),
            Alice(16 * 24, 16 * 33),

        ]

        print(str(state.npcs))
        self.stop_music()
        if state.musicOn:
            self.initialize_music()
        super().start(state)

    def update(self, state: "GameState"):
        self.clock.tick(60)
        controller = state.controller
        player = state.player
        controller.update()
        if controller.isExitPressed:
            state.isRunning = False

        player.update(state)
        for npc in state.npcs:
            npc.update(state)
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
        super().draw(state)  # This would handle drawing the tiled map and filling the screen

        # Drawing NPCs specific to this screen
        for npc in state.npcs:
            npc.draw(state)

        # Drawing the player
        state.player.draw(state)

        # Optionally drawing player stats if a specific key is pressed
        if state.controller.isPPressed:
            state.player.draw_player_stats(state)
            if state.controller.isBPressed:
                if state.controller.isPPressed:
                    state.controller.isPPressed = False
                    print("Mew")  # Reset the press state and provide feedback

        pygame.display.update()
