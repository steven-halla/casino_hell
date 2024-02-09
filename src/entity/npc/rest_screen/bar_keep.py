import math

import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class BarKeep(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.textbox = ShopNpcTextBox(
            [
             "Welcome, take a look at my stuff"],
            (50, 450, 50, 45), 30, 500)
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        # New: Initialize an array of items for the shopkeeper
        self.shop_items = ["beer", "moldy sandwich", "b key"]

        self.shop_costs = ["100", "200", "500"]

        self.barcutscene1 = False
        self.barcutscene2 = False

        self.selected_item_index = 0  # New attribute to track selected item index
        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Bartender.png").convert_alpha()
        self.selected_money_index = 0  # New attribute to track selected item index


    def show_shop(self, state: "GameState"):
        # This method passes the shop items to the textbox
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True


    def update(self, state: "GameState"):
        if state.restScreen.barscene1 == True:
            self.barcutscene1 = True
        if state.restScreen.barscene2 == True:
            self.barcutscene2 = True


        if "b key" in state.player.items:
            self.shop_items[2] = "sold out"

        if state.player.food < 1:
            self.shop_items[0] = "Your stomach can't handle more"
            self.shop_items[1] = "Your stomach can't handle more"
        elif state.player.food > 0:
            self.shop_items[0] = "beer"
            self.shop_items[1] = "moldy sandwich"


        if state.restScreen.barscene2 == True:
            self.barcutscene2 = True
        elif state.restScreen.barscene1 == True:
            self.barcutscene1 = True



        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            cost = int(self.shop_costs[self.selected_item_index])


            if state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
                self.input_time = pygame.time.get_ticks()
                state.player.canMove = True
                self.state = "waiting"
                print("Leaving the shop...")
                self.textbox.reset()
                if "+10 stamina" in state.player.items:
                    state.player.items.remove(" +10 stamina")
                    state.player.max_stamina_points += 10
                return

            if self.textbox.message_index == 0:
                if self.textbox.is_finished():

                    if state.controller.isUpPressed and pygame.time.get_ticks() - self.input_time > 400:
                        self.input_time = pygame.time.get_ticks()
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
                        # Increment the index but prevent it from exceeding the length of the list - 1
                        if self.selected_item_index < len(self.shop_items) - 1:
                            self.selected_item_index += 1
                            self.selected_money_index += 1
                        print(f"shop_items: {self.shop_items}")
                        print(f"shop_costs: {self.shop_costs}")
                        print(f"selected_item_index: {self.selected_item_index}")
                        print(f"selected_money_index: {self.selected_money_index}")

            if state.controller.isTPressed and pygame.time.get_ticks() - self.input_time > 500:
                self.input_time = pygame.time.get_ticks()
                selected_item = self.shop_items[self.selected_item_index]
                if state.player.money >= cost and state.player.food > 0 and self.textbox.is_finished():
                    if self.selected_money_index == 0:
                        print("hey 0")
                        state.player.money -= 100
                        state.player.stamina_points += 75
                        state.player.food -= 1
                        if state.player.stamina_points > state.player.max_stamina_points:
                            state.player.stamina_points = state.player.max_stamina_points
                            if self.barcutscene1 == False:
                                state.currentScreen = state.barCutScene1
                                state.barCutScene1.start(state)
                            elif self.barcutscene2 == False:
                                state.currentScreen = state.barCutScene2
                                state.barCutScene2.start(state)
                            elif self.barcutscene1 == True and self.barcutscene2 == True:
                                print("yay")



                    elif self.selected_money_index == 1:
                        state.player.money -= 100
                        print("hey 1")
                        # this will go above the max which is ok for this item
                        state.player.focus_points += 50
                        state.player.food -= 1
                        if state.player.focus_points > state.player.max_focus_points:
                            state.player.focus_points = state.player.max_focus_points
                            if self.barcutscene1 == False:
                                state.currentScreen = state.barCutScene1
                                state.barCutScene1.start(state)
                            elif self.barcutscene2 == False:
                                state.currentScreen = state.barCutScene2
                                state.barCutScene2.start(state)
                            elif self.barcutscene1 == True and self.barcutscene2 == True:
                                print("yay")

                    elif self.selected_money_index == 2:

                        if "b key" not in state.player.items:
                            state.player.money -= 500
                            state.player.items.append("b key")
                        print("Its boss time")


            self.update_talking(state)



    def update_waiting(self, state: "GameState"):
        player = state.player

        if state.controller.isTPressed and (
                pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            # print("distance: " + str(distance))

            if distance < 100:
                # print("start state: talking")

                self.state = "talking"

                self.state_start_time = pygame.time.get_ticks()
                # the below is where kenny had it
                self.textbox.reset()



    def update_talking(self, state: "GameState"):
        self.textbox.update(state)
        self.show_shop(state)

        if state.controller.isTPressed and self.textbox.is_finished():
            # Exiting the shop conversation
            # self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            # Allow the player to move again (new)
            # state.player.canMove = True  # Ensure this attribute exists in your Player class
            # self.textbox.reset()
        else:
            # While in conversation, prevent the player from moving (new)
            state.player.canMove = False

        cost = int(self.shop_costs[self.selected_item_index])
        # print(f"Currently selected item index: {self.selected_item_index}, Cost: {cost}")


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