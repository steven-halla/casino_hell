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
        bomb_x, bomb_y = 10, 20

        # sprite is the entire sprite sheet
        # sprite_sheet_full = self.slot_images_sprite_sheet.subsurface(pygame.Rect(1, 1, 500, 350))
        bomb_sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(450,100, 50,52))

        # Blit the subsurface onto the state.DISPLAY at coordinates (x, y)
        state.DISPLAY.blit(bomb_sprite, (bomb_x, bomb_y))

        lucky_seven_x , lucky_seven_y = 100, 20
        lucky_seven_sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(300,30, 60,60))
        # self.slot_images_sprite_sheet.subsurface(pygame.Rect(450, 100, 50, 52))
        state.DISPLAY.blit(lucky_seven_sprite, (lucky_seven_x, lucky_seven_y))


        dice_x, dice_y = 181, 20
        dice_sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(350, 100, 50, 52))
        # self.slot_images_sprite_sheet.subsurface(pygame.Rect(450, 100, 50, 52))
        state.DISPLAY.blit(dice_sprite, (dice_x, dice_y))

        coin_x, coin_y = 240, 20
        coin_sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(20,30, 75, 52))
        state.DISPLAY.blit(coin_sprite, (coin_x, coin_y))

        diamond_x, diamond_y = 320, 20
        diamond_sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(20, 170, 75, 52))
        state.DISPLAY.blit(diamond_sprite, (diamond_x, diamond_y))

        crown_x, crown_y = 400, 20
        crown_sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(15, 275, 80, 52))
        state.DISPLAY.blit(crown_sprite, (crown_x, crown_y))

        chest_x, chest_y = 500, 20
        chest_sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(300, 275, 75, 58))
        state.DISPLAY.blit(chest_sprite, (chest_x, chest_y))

        cherry_x, cherry_y = 20, 80
        cherry_sprite = self.slot_images_sprite_sheet.subsurface(pygame.Rect(120, 210, 75, 58))
        state.DISPLAY.blit(cherry_sprite, (cherry_x, cherry_y))





        pygame.display.flip()

        # It's usually better to call pygame.display.flip() once after all draw methods
















