import math

import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment
from game_constants.events import Events
from game_constants.treasure import Treasure


class Area2BarKeep(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.font = pygame.font.Font(None, 36)
        self.buy_sound = pygame.mixer.Sound("./assets/music/BFBuyingSelling.wav")  # Adjust the path as needed
        self.buy_sound.set_volume(0.3)

        self.cant_buy_sound = pygame.mixer.Sound("./assets/music/cantbuy3.wav")  # Adjust the path as needed
        self.cant_buy_sound.set_volume(0.5)

        self.menu_movement_sound = pygame.mixer.Sound("./assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
        self.menu_movement_sound.set_volume(0.2)

        self.textbox = ShopNpcTextBox(
            [
                ""],
            (50, 450, 50, 45), 30, 500)
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        # New: Initialize an array of items for the shopkeeper
        self.shop_items = [ "Hoppy Brew", "Carrion Nachos"]

        self.shop_costs = ["200", "200"]

        self.selected_item_index = 0  # New attribute to track selected item index
        self.character_sprite_image = pygame.image.load(
            "./assets/images/SNES - Harvest Moon - Bartender.png").convert_alpha()
        self.selected_money_index = 0  # New attribute to track selected item index

    def show_shop(self, state: "GameState"):
        # This method passes the shop items to the textbox
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True

    def update(self, state: "GameState"):


        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":

            state.player.hide_player = True


            if state.controller.isTPressed and state.player.food > 0:
                state.controller.isTPressed = False


                if self.selected_money_index == 0 and state.player.money < 500:

                    self.cant_buy_sound.play()  # Play the sound effect once


                elif self.selected_money_index == 0 and state.player.food < 1:
                    self.cant_buy_sound.play()  # Play the sound effect once


                elif self.selected_money_index == 1 and state.player.money < 500:
                    self.cant_buy_sound.play()  # Play the sound effect once

                elif self.selected_money_index == 1 and state.player.food < 1:
                    self.cant_buy_sound.play()  # Play the sound effect once

                elif self.selected_money_index == 1 and state.player.body < 2:
                    self.cant_buy_sound.play()  # Play the sound effect once



                if self.selected_item_index == 0 and state.player.money > 500:
                    self.buy_sound.play()  # Play the sound effect once

                    # print("mew")
                    state.player.money -= 200
                    state.player.stamina_points += 400
                    if state.player.stamina_points > state.player.max_stamina_points:
                        state.player.stamina_points = state.player.max_stamina_points
                    state.player.focus_points += 400
                    if state.player.focus_points > state.player.max_focus_points:
                        state.player.focus_points = state.player.max_focus_points
                    state.player.food -= 1

                    if Treasure.INVITATION.value in state.player.quest_items and Treasure.RIB_DEMON_KEY.value not in state.player.quest_items:
                        print("Your invited")
                        state.currentScreen = state.area2BarCutScene1
                        state.area2BarCutScene1.start(state)

                    elif Events.NUGGIE_SAUCE_1_FOUND.value in state.player.quest_items and Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value not in state.player.items:
                        print("Your invited")
                        state.currentScreen = state.area2BarCutScene2
                        state.area2BarCutScene2.start(state)
                        state.player.companions.append("erika")

                    elif Events.SPIRIT_TWO_ALICE_QUEST.value in state.player.quest_items and Events.SPIRIT_TWO_ALICE_QUEST_FINISHED.value not in state.player.level_two_npc_state:
                        state.currentScreen = state.area2BarCutScene3
                        state.area2BarCutScene3.start(state)



                elif self.selected_item_index == 1 and state.player.money > 500 and state.player.body == 2:
                    self.buy_sound.play()  # Play the sound effect once
                    state.player.money -= 200
                    state.player.luck += 1
                    state.player.enhanced_luck = True
                    state.player.food -= 1

                    if Treasure.INVITATION.value in state.player.quest_items and Treasure.RIB_DEMON_KEY.value not in state.player.quest_items:
                        print("Your invited")

                        state.currentScreen = state.area2BarCutScene1
                        state.area2BarCutScene1.start(state)

                    elif Events.NUGGIE_SAUCE_1_FOUND.value in state.player.quest_items and Equipment.DARLENES_CHICKEN_NUGGER_AMULET.value not in state.player.items:
                        print("Your invited")
                        state.currentScreen = state.area2BarCutScene2
                        state.area2BarCutScene2.start(state)
                        state.player.companions.append("erika")

                    elif Events.SPIRIT_TWO_ALICE_QUEST.value in state.player.quest_items and Events.SPIRIT_TWO_ALICE_QUEST_FINISHED.value not in state.player.level_two_npc_state:
                        state.currentScreen = state.area2BarCutScene3
                        state.area2BarCutScene3.start(state)

            cost = int(self.shop_costs[self.selected_item_index])

            if state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
                self.input_time = pygame.time.get_ticks()
                self.state = "waiting"
                state.controller.isBPressed = False

                # Allow the player to move after leaving the shop
                state.player.hide_player = False
                state.player.canMove = True
                self.textbox.reset()

            if self.textbox.message_index == 0 and self.textbox.is_finished():

                if state.controller.isTPressed:
                    state.controller.isTPressed = False



                if state.controller.isUpPressed and pygame.time.get_ticks() - self.input_time > 400:
                    self.input_time = pygame.time.get_ticks()
                    self.menu_movement_sound.play()  # Play the sound effect once

                    # Decrement the index but prevent it from going below 0
                    if self.selected_item_index > 0:
                        self.selected_item_index -= 1
                        self.selected_money_index -= 1
                    print(f"shop_items: {self.shop_items}")
                    print(f"shop_costs: {self.shop_costs}")
                    print(f"selected_item_index: {self.selected_item_index}")
                    print(f"selected_money_index: {self.selected_money_index}")

                elif state.controller.isDownPressed and pygame.time.get_ticks() - self.input_time > 400:
                    self.input_time = pygame.time.get_ticks()
                    self.menu_movement_sound.play()  # Play the sound effect once

                    # Increment the index but prevent it from exceeding the length of the list - 1
                    if self.selected_item_index < len(self.shop_items) - 1:
                        self.selected_item_index += 1
                        self.selected_money_index += 1
                    print(f"shop_items: {self.shop_items}")
                    print(f"shop_costs: {self.shop_costs}")
                    print(f"selected_item_index: {self.selected_item_index}")
                    print(f"selected_money_index: {self.selected_money_index}")

            self.update_talking(state)


    def update_waiting(self, state: "GameState"):
        player = state.player



        if state.controller.isTPressed and (
                pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                        player.collision.y - self.collision.y) ** 2)
            # print("distance: " + str(distance))

            if distance < 100 and state.player.menu_paused == False:
                # print("start state: talking")

                self.state = "talking"
                state.controller.isTPressed = False

                self.state_start_time = pygame.time.get_ticks()
                # the below is where kenny had it
                self.textbox.reset()

    def update_talking(self, state: "GameState"):
        self.textbox.update(state)
        self.show_shop(state)

        if state.controller.isTPressed and self.textbox.is_finished():
            # Exiting the shop conversation, reset to waiting state and allow movement
            self.state = "waiting"
            self.textbox.reset()  # Reset the textbox
            return  # Ensure no further code is executed in this method

            # During the conversation, prevent movement
        if self.state == "talking":
            state.player.canMove = False

        # If already in 'waiting' state, ensure player can move
        if self.state == "waiting":
            state.player.canMove = True

        # Prevent movement during conversation

    def draw(self, state):
        sprite_rect = pygame.Rect(5, 6, 23, 30)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        # rect = (
        # self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        # self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "waiting":
            pass
        elif self.state == "talking":
            # print("is talking")
            self.textbox.draw(state)
            if self.state == "talking":
                # state.DISPLAY.blit(self.font.render(f"Hurry and buy something", True,
                #                                     (255, 255, 255)), (70, 460))



                if self.selected_item_index == 0:
                    state.DISPLAY.blit(self.font.render(f"Made from the vomit of  hopping gluttons.", True,
                                                        (255, 255, 255)), (70, 460))
                    state.DISPLAY.blit(self.font.render(f"Restores 150 HP and 75 Magic.", True,
                                                        (255, 255, 255)), (70, 510))


                if self.selected_item_index == 1 and state.player.body == 2:
                    state.DISPLAY.blit(self.font.render(f"Nachos with extra maggots. ", True,
                                                        (255, 255, 255)), (70, 460))


                    state.DISPLAY.blit(self.font.render(f" Adds +1 luck till next rest. ", True,
                                                        (255, 255, 255)), (70, 510))

                elif self.selected_item_index == 1 and state.player.body == 1:
                    state.DISPLAY.blit(self.font.render(f"You need a body of 2 to eat or you'll barf it up. ", True,
                                                        (255, 255, 255)), (70, 460))






