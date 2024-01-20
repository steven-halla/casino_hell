import math

import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox


class BarKeep(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.textbox = ShopNpcTextBox(
            ["I'm the bar keeper. feel free to buy some beer if your body is 1",
             "Press B to leave, T to buy. Beer raises stamina by 50"],
            (50, 450, 50, 45), 30, 500)
        self.nohealthbox = NpcTextBox(
            ["Boy, you are not man enough to drink. Come back when your health is at least a 1. Sometiems you gain stats on a level up"],
            (50, 450, 700, 130),  # Position and size
            36,  # Font size
            500  # Delay
        )
        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.input_time = pygame.time.get_ticks()

        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"
        # New: Initialize an array of items for the shopkeeper
        self.shop_items = ["beer"]
        self.shop_costs = ["100"]
        self.selected_item_index = 0  # New attribute to track selected item index
        self.selected_money_index = 0  # New attribute to track selected item index



    def show_shop(self, state: "GameState"):
        # This method passes the shop items to the textbox
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True
        print("better now")

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)

        elif self.state == "talking":


            cost = int(self.shop_costs[self.selected_item_index])
            # print(f"Selected item index: {self.selected_item_index}, Cost: {cost}")

            # Handle 'B' press for leaving the shop
            if state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
                self.input_time = pygame.time.get_ticks()


                # Allow the player to move again
                state.player.canMove = True

                # Reset the selected item index
                ShopNpcTextBox.reset(state)

                # Transition the state back to "waiting"
                self.state = "waiting"
                print("Leaving the shop...")
                self.textbox.reset()  # Reset the textbox
                return  # Exit early to ensure no further processing in this update cycle



            elif state.controller.isUpPressed and pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.selected_item_index = (self.selected_item_index - 1) % len(self.shop_items)
                    print(f"Selected item index: {self.selected_item_index}")
                    print(f"Selected item index after pressing up: {self.selected_item_index}")


            elif state.controller.isDownPressed and pygame.time.get_ticks() - self.input_time > 500:
                self.input_time = pygame.time.get_ticks()
                self.selected_item_index = (self.selected_item_index + 1) % len(self.shop_items)
                print(f"Selected item index: {self.selected_item_index}")

            elif state.player.body > 0 and state.controller.isTPressed and pygame.time.get_ticks() - self.input_time > 500:
                self.input_time = pygame.time.get_ticks()

                # Check if the player has enough money
                if state.player.money >= cost and self.textbox.is_finished():
                    # Subtract the cost from the player's money
                    if state.player.stamina_points < state.player.max_stamina_points:
                        state.player.money -= cost

                        state.player.stamina_points += 50
                        if state.player.stamina_points > state.player.max_stamina_points:
                            state.player.stamina_points = state.player.max_stamina_points
                        selected_item = self.shop_items[self.selected_item_index]
                        state.player.items.append(selected_item)
                        print(f"Item purchased: {selected_item}. Remaining money: {state.player.money}")
                        print("Your inventory as it stands: " + str(state.player.items))
                    else:
                        print("Not enough money to purchase item.")

                # No need to transition the state back to "waiting" after purchase
                # as the player might want to continue shopping
            # elif state.player.body == 0 and state.controller.isTPressed and pygame.time.get_ticks() - self.input_time > 500:
            #     self.input_time = pygame.time.get_ticks()
            #     state.controller.isTPressed = False
            #     print("Hifasd")
            #
            #     # Allow the player to move again
            #     state.player.canMove = True
            #
            #     # Reset the selected item index
            #     NpcTextBox.reset(state)
            #
            #     # Transition the state back to "waiting"
            #     # self.state = "talking"
            #
            #     print("Leaving the shop...")
            #     self.nohealthbox.reset()  # Reset the textbox
            #     return  # Exit early to ensure no further processing in this update cycle
            elif state.player.body == 0 and state.controller.isTPressed and pygame.time.get_ticks() - self.input_time > 500:
                self.input_time = pygame.time.get_ticks()
                # state.controller.isTPressed = False  # You might not need this line if it interferes with the detection of the 'T' press
                state.controller.isTPressed = False
                print("Hifasd")  # This print statement seems like a placeholder, consider updating or removing it.

                # Allow the player to move again
                state.player.canMove = True

                # Reset the selected item index
                NpcTextBox.reset(state)

                # Transition the state back to "waiting"
                # self.state = "talking"  # This line seems commented out; ensure your state management is correct.

                print("Leaving the shop...")
                self.nohealthbox.reset()  # Reset the textbox

                return

            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player

        if state.controller.isTPressed and (
                pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            # print("distance: " + str(distance))

            if distance < 100 and state.player.body > 0:
                # print("start state: talking")

                self.state = "talking"

                self.state_start_time = pygame.time.get_ticks()
                # the below is where kenny had it
                self.textbox.reset()
            elif distance < 100 and state.player.body == 0:
                self.state = "talking"
                self.state_start_time = pygame.time.get_ticks()
                self.nohealthbox.reset()





    def update_talking(self, state: "GameState"):
        if state.player.body > 0:
            self.textbox.update(state)
            self.show_shop(state)
        elif state.player.body == 0:
            self.nohealthbox.update(state)

        if state.player.body > 0 and state.controller.isTPressed and self.textbox.is_finished():
            # Exiting the shop conversation
            # self.state = "waiting"
            self.state_start_time = pygame.time.get_ticks()
            # Allow the player to move again (new)
            # state.player.canMove = True  # Ensure this attribute exists in your Player class
            # self.textbox.reset()
        elif state.player.body == 0 and state.controller.isTPressed and self.nohealthbox.is_finished():
            self.state_start_time = pygame.time.get_ticks()
            self.state = "talking"
            state.player.canMove = True
        else:
            # While in conversation, prevent the player from moving (new)
            state.player.canMove = False

        cost = int(self.shop_costs[self.selected_item_index])
        # print(f"Currently selected item index: {self.selected_item_index}, Cost: {cost}")


    def draw(self, state):
        rect = (
        self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        self.collision.width, self.collision.height)
        pygame.draw.rect(state.DISPLAY, self.color, rect)

        if self.state == "waiting":
            pass
        elif self.state == "talking":
            # print("is talking")
            if state.player.body > 0:
                self.textbox.draw(state)
            elif state.player.body == 0:
                print("am i drawing")
                self.nohealthbox.draw(state)