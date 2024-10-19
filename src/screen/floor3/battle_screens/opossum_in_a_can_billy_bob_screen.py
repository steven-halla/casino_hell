import pygame

from entity.gui.screen.gamble_screen import GambleScreen


class OpossumInACanBillyBobScreen(GambleScreen):
    def __init__(self, screenName: str = "Opossum in a can Billy Bob") -> None:
        super().__init__(screenName)
        self.bet: int = 100
        self.game_state:str = self.WELCOME_SCREEN



    def opossum_game_reset(self):
        pass
    def opossum_round_reset(self):
        pass

    def update(self, state):
        super().update(state)

    def draw(self, state):
        super().draw(state)
        self.draw_hero_info_boxes(state)
        self.draw_enemy_info_box(state)
        self.draw_bottom_black_box(state)

        pygame.display.flip()




