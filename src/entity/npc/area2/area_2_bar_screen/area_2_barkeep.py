import math

import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.treasure import Treasure


class Area2BarKeep(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.font = pygame.font.Font(None, 36)
        self.buy_sound = pygame.mixer.Sound("./assets/music/BFBuyingSelling.wav")
        self.buy_sound.set_volume(0.3)
        self.cant_buy_sound = pygame.mixer.Sound("./assets/music/cantbuy3.wav")
        self.cant_buy_sound.set_volume(0.5)
        self.menu_movement_sound = pygame.mixer.Sound("./assets/music/1BItemMenuItng.wav")
        self.menu_movement_sound.set_volume(0.2)

        self.textbox = ShopNpcTextBox([""], (50, 450, 50, 45), 30, 500)
        self.state_start_time = pygame.time.get_ticks()
        self.input_time = pygame.time.get_ticks()
        self.state = "waiting"

        self.shop_items = [
            "Hoppy Brew", "Carrion Nachos",
            "Body Feast", "Mind Feast", "Spirit Feast", "Luck Feast", "Perception Feast"
        ]
        self.shop_costs = ["200", "200"] + ["500"] * 5

        self.selected_item_index = 0
        self.character_sprite_image = pygame.image.load("./assets/images/SNES - Harvest Moon - Bartender.png").convert_alpha()
        self.selected_money_index = 0

    def show_shop(self, state: "GameState"):
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            state.player.hide_player = True

            # sold out logic
            if state.player.body == 2:
                self.shop_items[2] = "sold out"
            if state.player.mind == 2:
                self.shop_items[3] = "sold out"
            if state.player.spirit == 2:
                self.shop_items[4] = "sold out"
            if state.player.luck == 2:
                self.shop_items[5] = "sold out"
            if state.player.perception == 2:
                self.shop_items[6] = "sold out"

            if state.controller.isTPressed and state.player.food > 0:
                state.controller.isTPressed = False

                if self.selected_item_index == 0 and state.player.money >= 200:
                    self.buy_sound.play()
                    state.player.money -= 200
                    state.player.stamina_points = min(state.player.stamina_points + 400, state.player.max_stamina_points)
                    state.player.focus_points = min(state.player.focus_points + 400, state.player.max_focus_points)
                    state.player.food -= 1

                elif self.selected_item_index == 1 and state.player.money >= 200 and state.player.body == 2:
                    self.buy_sound.play()
                    state.player.money -= 200
                    state.player.luck += 1
                    state.player.enhanced_luck = True
                    state.player.food -= 1

                elif self.selected_item_index == 2 and state.player.body < 2 and state.player.money >= 500:
                    self.buy_sound.play()
                    state.player.body += 1
                    state.player.money -= 500

                elif self.selected_item_index == 3 and state.player.mind < 2 and state.player.money >= 500:
                    self.buy_sound.play()
                    state.player.mind += 1
                    state.player.money -= 500

                elif self.selected_item_index == 4 and state.player.spirit < 2 and state.player.money >= 500:
                    self.buy_sound.play()
                    state.player.spirit += 1
                    state.player.money -= 500

                elif self.selected_item_index == 5 and state.player.luck < 2 and state.player.money >= 500:
                    self.buy_sound.play()
                    state.player.luck += 1
                    state.player.money -= 500

                elif self.selected_item_index == 6 and state.player.perception < 2 and state.player.money >= 500:
                    self.buy_sound.play()
                    state.player.perception += 1
                    state.player.money -= 500

                else:
                    self.cant_buy_sound.play()

            if state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
                self.input_time = pygame.time.get_ticks()
                self.state = "waiting"
                state.controller.isBPressed = False
                state.player.hide_player = False
                state.player.canMove = True
                self.textbox.reset()

            if self.textbox.message_index == 0 and self.textbox.is_finished():
                if state.controller.isUpPressed and pygame.time.get_ticks() - self.input_time > 400:
                    self.input_time = pygame.time.get_ticks()
                    self.menu_movement_sound.play()
                    if self.selected_item_index > 0:
                        self.selected_item_index -= 1
                        self.selected_money_index -= 1

                elif state.controller.isDownPressed and pygame.time.get_ticks() - self.input_time > 400:
                    self.input_time = pygame.time.get_ticks()
                    self.menu_movement_sound.play()
                    if self.selected_item_index < len(self.shop_items) - 1:
                        self.selected_item_index += 1
                        self.selected_money_index += 1

            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt((state.player.collision.x - self.collision.x) ** 2 + (state.player.collision.y - self.collision.y) ** 2)
            if distance < 100 and state.player.menu_paused == False:
                self.state = "talking"
                state.controller.isTPressed = False
                self.state_start_time = pygame.time.get_ticks()
                self.textbox.reset()

    def update_talking(self, state: "GameState"):
        self.textbox.update(state)
        self.show_shop(state)
        if self.state == "talking":
            state.player.canMove = False
        if self.state == "waiting":
            state.player.canMove = True

    def draw(self, state):
        sprite_rect = pygame.Rect(5, 6, 23, 30)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        if self.state == "talking":
            self.textbox.draw(state)
            descriptions = [
                ["Made from the vomit of hopping gluttons.", "Restores 150 HP and 75 Magic."],
                ["Nachos with extra maggots.", "Adds +1 luck till next rest." if state.player.body == 2 else "You need a body of 2 to eat or you'll barf."],
                ["A heavy meal.", "Boosts body stat by 1."],
                ["Brainy stew.", "Boosts mind stat by 1."],
                ["Mystic soup.", "Boosts spirit stat by 1."],
                ["Lucky curry.", "Boosts luck stat by 1."],
                ["Eyeball pie.", "Boosts perception stat by 1."]
            ]
            if self.selected_item_index < len(descriptions):
                for i, line in enumerate(descriptions[self.selected_item_index]):
                    state.DISPLAY.blit(self.font.render(line, True, (255, 255, 255)), (70, 460 + i * 50))
