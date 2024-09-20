import math

import pygame

from entity.gui.textbox.shop_npc_text_box import ShopNpcTextBox
from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.equipment import Equipment


class Area2ShopKeeper(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.font = pygame.font.Font(None, 36)
        self.buy_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/BFBuyingSelling.wav")  # Adjust the path as needed
        self.buy_sound.set_volume(0.3)

        self.cant_buy_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/cantbuy3.wav")  # Adjust the path as needed
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
        self.shop_items = ["COIN_SAVE_AREA_2", "Hippo Hour Glass", "HEALTHY_GLOVES", "STAT_POTION_AREA_2"]

        self.shop_costs = ["200", "500", "1000", "1000"]

        self.selected_item_index = 0  # New attribute to track selected item index
        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Tool Shop Owner.png").convert_alpha()
        self.selected_money_index = 0  # New attribute to track selected item index
        self.stat_point_increase = False


    def show_shop(self, state: "GameState"):
        # This method passes the shop items to the textbox
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True


    def update(self, state: "GameState"):


        if self.state == "waiting":
            self.update_waiting(state)
            state.player.canMove = True
        elif self.state == "talking":
            state.player.hide_player = True

            if Equipment.COIN_SAVE_AREA_2.value in state.player.level_two_npc_state:
                self.shop_items[0] = "sold out"

            if Equipment.HIPPO_HOUR_GLASS.value in state.player.level_two_npc_state:
                self.shop_items[1] = "sold out"

            if Equipment.HEALTHY_GLOVES.value in state.player.level_two_npc_state:
                self.shop_items[2] = "sold out"

            if Equipment.STAT_POTION_AREA_2.value in state.player.level_two_npc_state:
                self.shop_items[3] = "sold out"



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

                if state.controller.isTPressed:
                    state.controller.isTPressed = False


                    if state.player.money > 899 and self.selected_item_index == 0 and Equipment.COIN_SAVE_AREA_2.value not in state.player.level_two_npc_state:
                        print("HI")
                        Equipment.COIN_SAVE_AREA_2.add_equipment_to_player(state.player, Equipment.COIN_SAVE_AREA_2)
                        state.player.money -= 200
                        state.save_game(state.player, state)  # Call the save_game function

                    if state.player.money > 1199 and self.selected_item_index == 1 and Equipment.HIPPO_HOUR_GLASS.value not in state.player.level_two_npc_state:
                        print("HIPPOOOOOOOOOOOOOO")
                        Equipment.HIPPO_HOUR_GLASS.add_equipment_to_player(state.player, Equipment.HIPPO_HOUR_GLASS)
                        state.player.money -= 500
                        print(state.player.level_two_npc_state)



                    if state.player.money > 1699 and self.selected_item_index == 2 and Equipment.HEALTHY_GLOVES.value not in state.player.level_two_npc_state:
                        print("HI")
                        Equipment.HEALTHY_GLOVES.add_equipment_to_player(state.player, Equipment.HEALTHY_GLOVES)
                        state.player.money -= 1000

                    if state.player.money > 1699 and self.selected_item_index == 3 and Equipment.STAT_POTION_AREA_2.value not in state.player.level_two_npc_state:
                        print("HI")
                        Equipment.STAT_POTION_AREA_2.add_equipment_to_player(state.player, Equipment.STAT_POTION_AREA_2)
                        state.player.money -= 1000
                        self.stat_point_increase = True


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


            self.update_talking(state)

    def sold_out(self, item_index: int):
        # Mark the item as sold out
        self.shop_items[item_index] = "sold out"

    def update_waiting(self, state: "GameState"):
        player = state.player

        player.hide_player = False

        if state.controller.isTPressed and (
                pygame.time.get_ticks() - self.state_start_time) > 500 and state.player.menu_paused == False:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            # print("distance: " + str(distance))

            if distance < 100 :
                state.controller.isTPressed = False
                # print("start state: talking")

                self.state = "talking"

                self.state_start_time = pygame.time.get_ticks()
                # the below is where kenny had it
                self.textbox.reset()



    def update_talking(self, state: "GameState"):
        self.textbox.update(state)
        self.show_shop(state)
        state.player.canMove = False

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

        if self.state == "waiting":
            pass
        elif self.state == "talking":
            self.textbox.draw(state)
            if self.state == "talking":
                # Handle drawing the shop interaction text

                if self.stat_point_increase == True:
                    # Draw a box on the far right end of the screen, 400 pixels wide and 400 pixels high
                    box_width = 250
                    box_height = 250
                    border_width = 5
                    start_x = state.DISPLAY.get_width() - box_width - 25  # Far right of the screen
                    start_y = state.DISPLAY.get_height() // 2 - box_height // 2  # Centered vertically

                    # Create the black box
                    black_box = pygame.Surface((box_width, box_height))
                    black_box.fill((0, 0, 0))

                    # Create a white border
                    white_border = pygame.Surface(
                        (box_width + 2 * border_width, box_height + 2 * border_width)
                    )
                    white_border.fill((255, 255, 255))
                    white_border.blit(black_box, (border_width, border_width))

                    # Draw the box on the far right
                    state.DISPLAY.blit(white_border, (start_x - border_width, start_y - border_width))

                    # You can also draw text or options inside the box if needed
                    state.DISPLAY.blit(self.font.render("Max Value 2:", True, (255, 255, 255)), (start_x + 10, start_y + 20))

                    # You can add more drawing logic for the stat choices inside this box
                    # For example, you can draw a list of stats like:
                    stats = ["Body", "Mind", "Spirit", "Perception", "Luck"]
                    for idx, stat in enumerate(stats):
                        y_position = start_y + 60 + idx * 40  # Adjust vertical spacing
                        state.DISPLAY.blit(self.font.render(stat, True, (255, 255, 255)), (start_x + 60, y_position))
