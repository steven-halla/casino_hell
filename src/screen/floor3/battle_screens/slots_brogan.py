import pygame

from entity.gui.screen.gamble_screen import GambleScreen


class SlotsBrogan(GambleScreen):
    def __init__(self, screenName: str = "Slots") -> None:
        super().__init__(screenName)
        self.game_state: str = self.WELCOME_SCREEN
        self.dealer_name: str = "Brogan"
        self.slot_images_sprite_sheet: pygame.Surface = pygame.image.load("./assets/images/slots_images_trans.png")

        self.spell_sound: pygame.mixer.Sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/spell_sound.mp3")  # Adjust the path as needed
        self.spell_sound.set_volume(0.3)
        self.magic_screen_choices: list[str] = []
        self.bet_screen_choices: list[str] = ["Back"]
        self.magic_screen_index: int = 0
        self.bet: int = 50
        pygame.mixer.music.stop()
        self.magic_lock: bool = False
        self.blit_message_x: int = 65
        self.blit_message_y: int = 460
        self.brogan_bankrupt: int = 0
        self.player_stamina_med_cost: int = 5
        self.player_stamina_high_cost: int = 10  # useing higher bet option
        self.lock_down_inactive: int = 0

    def start(self, state: 'GameState'):
        pass

    def reset_slots_game(self):
        pass
    def reset_slots_round(self):
        pass

    def update(self,  state):
        # print(self.game_state)
        controller = state.controller
        controller.update()
        state.player.update(state)
        super().update(state)

    def draw(self, state):
        super().draw(state)

        # Set the coordinates for the sprite
        sprite_data = {
            "bomb": ((10, 20), (450, 100, 50, 52)),
            "lucky_seven": ((100, 20), (300, 30, 60, 60)),
            "dice": ((181, 20), (350, 100, 50, 52)),
            "coin": ((240, 20), (20, 30, 75, 52)),
            "diamond": ((320, 20), (20, 170, 75, 52)),
            "crown": ((400, 20), (15, 275, 80, 52)),
            "chest": ((500, 20), (300, 275, 75, 58)),
            "cherry": ((20, 80), (120, 210, 75, 58)),
            "dice_6": ((120, 80), (400, 210, 50, 58)),
            "spin": ((200, 80), (40, 110, 52, 58)),
        }

        # Loop through the dictionary and blit each sprite
        for name, (blit_coords, sprite_rect) in sprite_data.items():
            sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(*sprite_rect))
            state.DISPLAY.blit(sprite, blit_coords)




        pygame.display.flip()

        # It's usually better to call pygame.display.flip() once after all draw methods
















