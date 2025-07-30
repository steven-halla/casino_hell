import math
import pygame
from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.treasure import Treasure


class Area1BarKeep(Npc):
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
        self.all_items = ["Hoppy Brew", "Carrion Nachos"]
        self.all_costs = ["200", "200"]
        self.shop_items = []
        self.shop_costs = []
        self.selected_item_index = 0
        self.character_sprite_image = pygame.image.load(
            "./assets/images/SNES - Harvest Moon - Bartender.png").convert_alpha()
        self.selected_money_index = 0

    def show_shop(self, state: "GameState"):
        self.shop_items = [self.all_items[0]]
        self.shop_costs = [self.all_costs[0]]

        if state.player.body == 0:
            self.shop_items.append(self.all_items[1])
            self.shop_costs.append(self.all_costs[1])

        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            state.player.hide_player = True

            if state.controller.isTPressed and state.player.food > 0:
                state.controller.isTPressed = False

                if state.player.money < 200:
                    self.cant_buy_sound.play()

                elif self.selected_item_index == 0:
                    self.buy_sound.play()
                    state.player.money -= 200
                    state.player.stamina_points += 50
                    if state.player.stamina_points > state.player.max_stamina_points:
                        state.player.stamina_points = state.player.max_stamina_points + 50
                    state.player.focus_points += 25
                    if state.player.focus_points > state.player.max_focus_points:
                        state.player.focus_points = state.player.max_focus_points + 25
                    state.player.food -= 1



            elif state.controller.confirm_button and self.selected_item_index == 1:
                if state.player.money < 200:
                    self.cant_buy_sound.play()
                else:
                    self.buy_sound.play()
                    state.player.money -= 200
                    # state.player.food -= 1
                    state.player.body += 1



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
        player = state.player
        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.hypot(player.collision.x - self.collision.x, player.collision.y - self.collision.y)
            if distance < 100 and not state.player.menu_paused:
                self.state = "talking"
                state.controller.isTPressed = False
                self.state_start_time = pygame.time.get_ticks()
                self.textbox.reset()

    def update_talking(self, state: "GameState"):
        self.textbox.update(state)
        self.show_shop(state)

        if state.controller.isTPressed and self.textbox.is_finished():
            self.state = "waiting"
            self.textbox.reset()
            return

        if self.state == "talking":
            state.player.canMove = False
        elif self.state == "waiting":
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
            if self.selected_item_index == 0:
                state.DISPLAY.blit(self.font.render("Made from the vomit of hopping gluttons.", True, (255, 255, 255)), (70, 460))
                state.DISPLAY.blit(self.font.render("Restores 150 HP and 75 Magic.", True, (255, 255, 255)), (70, 510))
            elif len(self.shop_items) > 1 and self.selected_item_index == 1:
                state.DISPLAY.blit(self.font.render("Nachos with extra maggots.", True, (255, 255, 255)), (70, 460))
                state.DISPLAY.blit(self.font.render("Adds +1 body permanently.", True, (255, 255, 255)), (70, 510))
