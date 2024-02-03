import math

import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class ShopKeeper(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.textbox = ShopNpcTextBox(
            [
             "Welcome to my humble shop. Feel free to browse my humble weares. Press B to leave, T to buy"],
            (50, 450, 50, 45), 30, 500)
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        # New: Initialize an array of items for the shopkeeper
        self.shop_items = ["+10 stamina", "save coin", "opossum repellent"]

        self.shop_costs = ["100", "200", "300"]

        self.selected_item_index = 0  # New attribute to track selected item index
        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Tool Shop Owner.png").convert_alpha()
        self.selected_money_index = 0  # New attribute to track selected item index


    def show_shop(self, state: "GameState"):
        # This method passes the shop items to the textbox
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True


    def update(self, state: "GameState"):


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
                    state.player.items.remove("+10 stamina")
                    state.player.max_stamina_points += 10
                return

            if self.textbox.message_index == 0:
                if state.controller.isUpPressed and pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    # Decrement the index but prevent it from going below 0
                    if self.selected_item_index > 0:
                        self.selected_item_index -= 1
                        self.selected_money_index -= 1
                    print(f"shop_items: {self.shop_items}")
                    print(f"shop_costs: {self.shop_costs}")
                    print(f"selected_item_index: {self.selected_item_index}")
                    print(f"selected_money_index: {self.selected_money_index}")

                elif state.controller.isDownPressed and pygame.time.get_ticks() - self.input_time > 500:
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
                if state.player.money >= cost and selected_item != "sold out" and self.textbox.is_finished():
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