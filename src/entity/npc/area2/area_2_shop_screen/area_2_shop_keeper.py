import math
import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.magic import Magic


class Area2ShopKeeper(Npc):
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
            Equipment.COIN_SAVE_AREA_2.value,
            Equipment.HIPPO_HOUR_GLASS.value,
            Equipment.HEALTHY_GLOVES.value,
            Events.STAT_POTION_AREA_2.value,
            Equipment.BOSS_KEY.value
        ]
        self.shop_costs = ["500", "500", "500", "500", "500"]
        self.selected_item_index = 0
        self.character_sprite_image = pygame.image.load(
            "./assets/images/SNES - Harvest Moon - Tool Shop Owner.png").convert_alpha()
        self.selected_money_index = 0
        self.stat_point_increase = False
        self.stat_point_increase_index = 0
        self.index_1_bought = False
        self.in_shop = False

    def show_shop(self, state: "GameState"):
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True

    def update(self, state: "GameState"):
        stats = ["Body", "Mind", "Spirit", "Perception", "Luck"]
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            state.player.hide_player = True

            if Equipment.COIN_SAVE_AREA_2.value in state.player.level_two_npc_state:
                self.shop_items[0] = "sold out"
            if Equipment.HIPPO_HOUR_GLASS.value in state.player.quest_items:
                self.shop_items[1] = "sold out"
            if Equipment.HEALTHY_GLOVES.value in state.player.level_two_npc_state:
                self.shop_items[2] = "sold out"
            if Events.STAT_POTION_AREA_2.value in state.player.level_two_npc_state:
                self.shop_items[3] = "sold out"
            if Equipment.BOSS_KEY.value in state.player.quest_items:
                self.shop_items[4] = "sold out"

            cost = int(self.shop_costs[self.selected_item_index])

            if (state.controller.isBPressed or state.controller.isBPressedSwitch) and pygame.time.get_ticks() - self.input_time > 500 and not self.stat_point_increase:
                self.input_time = pygame.time.get_ticks()
                self.state = "waiting"
                self.textbox.reset()
                self.stat_point_increase = False
                self.in_shop = False
                state.player.canMove = True

            if self.textbox.message_index == 0 and self.textbox.is_finished():
                if state.controller.confirm_button:
                    if self.selected_item_index == 0:
                        cost = 500
                        if state.player.money - cost < 500 or Equipment.COIN_SAVE_AREA_2.value in state.player.level_two_npc_state:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Equipment.add_equipment_to_player(state.player, Equipment.COIN_SAVE_AREA_2)
                            state.player.money -= cost
                    elif self.selected_item_index == 1:
                        cost = 500
                        if state.player.money - cost < 500 or Equipment.HIPPO_HOUR_GLASS.value in state.player.quest_items:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Equipment.add_equipment_to_player(state.player, Equipment.HIPPO_HOUR_GLASS)
                            state.player.money -= cost
                    elif self.selected_item_index == 2:
                        cost = 500
                        if state.player.money - cost < 500 or Equipment.HEALTHY_GLOVES.value in state.player.level_two_npc_state:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Equipment.add_equipment_to_player(state.player, Equipment.HEALTHY_GLOVES)
                            state.player.money -= cost
                    elif self.selected_item_index == 3:
                        cost = 500
                        if state.player.money - cost < 500 or Events.STAT_POTION_AREA_2.value in state.player.level_two_npc_state:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Events.add_event_to_player(state.player, Events.STAT_POTION_AREA_2)
                            state.player.money -= cost
                            self.stat_point_increase = True
                    elif self.selected_item_index == 4:
                        cost = 500
                        if state.player.money - cost < 500 or Equipment.BOSS_KEY.value in state.player.quest_items:
                            self.cant_buy_sound.play()
                        else:
                            self.buy_sound.play()
                            Equipment.add_equipment_to_player(state.player, Equipment.BOSS_KEY)
                            state.player.money -= cost

                if state.controller.isUpPressed and pygame.time.get_ticks() - self.input_time > 400 and not self.stat_point_increase:
                    self.input_time = pygame.time.get_ticks()
                    self.menu_movement_sound.play()
                    if self.selected_item_index > 0:
                        self.selected_item_index -= 1
                        self.selected_money_index -= 1
                elif state.controller.isDownPressed and pygame.time.get_ticks() - self.input_time > 400 and not self.stat_point_increase:
                    self.input_time = pygame.time.get_ticks()
                    self.menu_movement_sound.play()
                    if self.selected_item_index < len(self.shop_items) - 1:
                        self.selected_item_index += 1
                        self.selected_money_index += 1

            self.update_talking(state)

    def sold_out(self, item_index: int):
        self.shop_items[item_index] = "sold out"

    def update_waiting(self, state: "GameState"):
        player = state.player
        player.hide_player = False
        if state.controller.isTPressed and (pygame.time.get_ticks() - self.state_start_time) > 500 and not player.menu_paused:
            distance = math.sqrt((player.collision.x - self.collision.x) ** 2 + (player.collision.y - self.collision.y) ** 2)
            if distance < 100:
                state.controller.isTPressed = False
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                self.textbox.reset()

    def update_talking(self, state: "GameState"):
        self.textbox.update(state)
        self.show_shop(state)
        if state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
            self.input_time = pygame.time.get_ticks()
            self.state = "waiting"
            state.player.canMove = True
            self.textbox.reset()
        elif state.controller.isTPressed and self.textbox.is_finished():
            state.controller.isTPressed = False
            self.state = "waiting"
            state.player.canMove = True
            self.textbox.reset()
        if self.state == "talking":
            state.player.canMove = False
        elif self.state == "waiting":
            state.player.canMove = True

    def draw(self, state):
        sprite_rect = pygame.Rect(5, 6, 18, 25)
        sprite = self.character_sprite_image.subsurface(sprite_rect)
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        if self.state == "talking":
            self.textbox.draw(state)

            if self.selected_item_index == 2 and Equipment.HEALTHY_GLOVES.value not in state.player.level_two_npc_state:
                state.DISPLAY.blit(self.font.render("Boosts stamina by 30 when worn.", True, (255, 255, 255)), (70, 460))
                state.DISPLAY.blit(self.font.render("Good for keeping energy high!", True, (255, 255, 255)), (70, 510))
            elif self.selected_item_index == 2 and Equipment.HEALTHY_GLOVES.value in state.player.level_two_npc_state:
                state.DISPLAY.blit(self.font.render("Healthy Gloves already purchased!", True, (255, 255, 255)), (70, 460))
