import math

import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class ShopKeeper(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.font = pygame.font.Font(None, 36)
        self.buy_sound = pygame.mixer.Sound("./assets/music/BFBuyingSelling.wav")  # Adjust the path as needed
        self.buy_sound.set_volume(0.3)

        self.cant_buy_sound = pygame.mixer.Sound("./assets/music/cantbuy3.wav")  # Adjust the path as needed
        self.cant_buy_sound.set_volume(0.5)

        self.textbox = ShopNpcTextBox(
            [
             ""],
            (50, 450, 50, 45), 30, 500)
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        # New: Initialize an array of items for the shopkeeper
        self.shop_items = ["mega potion", "save coin", "opossum repellent"]

        self.shop_costs = ["100", "10", "300"]

        self.selected_item_index = 0  # New attribute to track selected item index
        self.character_sprite_image = pygame.image.load(
            "./assets/images/SNES - Harvest Moon - Tool Shop Owner.png").convert_alpha()
        self.selected_money_index = 0  # New attribute to track selected item index


    def show_shop(self, state: "GameState"):
        # This method passes the shop items to the textbox
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True


    def update(self, state: "GameState"):


        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":

            if "opossum repellent" in state.player.items:
                self.shop_items[2] = "sold out"
            if state.player.shop_keep_potion == True:
                self.shop_items[0] = "sold out"
            if state.player.shop_keep_save_coin == True:
                self.shop_items[1] = "sold out"

            cost = int(self.shop_costs[self.selected_item_index])


            if state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
                self.input_time = pygame.time.get_ticks()
                state.player.canMove = True
                self.state = "waiting"
                print("Leaving the shop...")
                self.textbox.reset()
                if "mega potion" in state.player.items:
                    state.player.items.remove("mega potion")
                    state.player.max_stamina_points += 10
                return

            if self.textbox.message_index == 0 and self.textbox.is_finished():
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
                if state.player.money >= cost and (state.player.money - cost >= 100) and selected_item != "sold out" and self.textbox.is_finished():
                    self.buy_sound.play()  # Play the sound effect once

                    state.player.money -= cost
                    if selected_item not in state.player.items:
                        state.player.items.append(selected_item)  # Append the selected item to the player's inventory only if it's not already there
                    else:
                        # If the item is already in the inventory, remove any multiples (keep only one)
                        state.player.items = [item for item in state.player.items if item != selected_item]
                        state.player.items.append(selected_item)
                    self.sold_out(self.selected_item_index)  # Mark the item as sold out
                    print(f"Item purchased: {selected_item}. Remaining money: {state.player.money}")
                    print("Your inventory as it stands: " + str(state.player.items))
                else:
                    if selected_item == "sold out":
                        print("This item is sold out.")

                    else:
                        print("Not enough money to purchase item.")

                if "save coin" in state.player.items:
                    state.player.items.remove("save coin")
                    state.player.shop_keep_save_coin = True
                    state.save_game(state.player, state)  # Call the save_game function


                if "mega potion" in state.player.items:
                    state.player.items.remove("mega potion")
                    state.player.max_stamina_points += 20
                    state.player.max_focus_points += 20
                    state.player.shop_keep_potion = True

                    print("taste yum yum")
            self.update_talking(state)

    def sold_out(self, item_index: int):
        # Mark the item as sold out
        self.shop_items[item_index] = "sold out"

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
        sprite_rect = pygame.Rect(5, 6, 18, 25)

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


                if self.selected_item_index == 0 and self.shop_items[0] == "sold out":
                    state.DISPLAY.blit(self.font.render(f"Potion is Sold out", True,
                                                        (255, 255, 255)), (70, 460))
                    if state.controller.isTPressed == True and self.textbox.is_finished() and pygame.time.get_ticks() - self.input_time > 150:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                elif self.selected_item_index == 0 and state.player.money < 200 and self.shop_items[0] != "sold out":
                    state.DISPLAY.blit(self.font.render(f"Money cannot fall below 100 post purchase", True,
                                                        (255, 255, 255)), (70, 460))
                    if state.controller.isTPressed == True and self.textbox.is_finished() and pygame.time.get_ticks() - self.input_time > 150:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                elif self.selected_item_index == 0:
                    state.DISPLAY.blit(self.font.render(f"Health and Magic max + 20", True,
                                                        (255, 255, 255)), (70, 460))


                if self.selected_item_index == 1 and self.shop_items[1] == "sold out":
                    state.DISPLAY.blit(self.font.render(f"Save Coin is Sold out", True,
                                                        (255, 255, 255)), (70, 460))
                    if state.controller.isTPressed == True and self.textbox.is_finished() and pygame.time.get_ticks() - self.input_time > 150:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                elif self.selected_item_index == 1 and state.player.money < 500 and self.shop_items[1] != "sold out":
                    state.DISPLAY.blit(self.font.render(f"Money cannot fall below 300 post purchase", True,
                                                        (255, 255, 255)), (70, 460))
                    if state.controller.isTPressed == True and self.textbox.is_finished() and pygame.time.get_ticks() - self.input_time > 150:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once
                elif self.selected_item_index == 1 and self.shop_items[0] != "sold out":
                    state.DISPLAY.blit(self.font.render(f"There is only one. It saves your game now upon purchase.  ", True,
                                                        (255, 255, 255)), (70, 460))

                if self.selected_item_index == 2 and self.shop_items[2] == "sold out":
                    state.DISPLAY.blit(self.font.render(f"Opossum Repelliant is Sold out", True,
                                                        (255, 255, 255)), (70, 460))
                    if state.controller.isTPressed == True and self.textbox.is_finished() and pygame.time.get_ticks() - self.input_time > 150:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                elif self.selected_item_index == 2 and state.player.money < 400:
                    state.DISPLAY.blit(self.font.render(f"Money cannot fall below 100 post purchase", True,
                                                        (255, 255, 255)), (70, 460))
                    if state.controller.isTPressed == True and self.textbox.is_finished() and pygame.time.get_ticks() - self.input_time > 150:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                elif self.selected_item_index == 2:
                    state.DISPLAY.blit(self.font.render(f"Halves damage of opossum bites in opossum in a can. ", True,
                                                        (255, 255, 255)), (70, 460))