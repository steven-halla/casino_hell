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
        self.buy_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/BFBuyingSelling.wav")  # Adjust the path as needed
        self.buy_sound.set_volume(0.3)

        self.cant_buy_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/cantbuy3.wav")  # Adjust the path as needed
        self.cant_buy_sound.set_volume(0.5)

        self.menu_movement_sound = pygame.mixer.Sound("/Users/stevenhalla/code/casino_hell/assets/music/1BItemMenuItng.wav")  # Adjust the path as needed
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
        self.shop_items = ["COIN_SAVE_AREA_2", "Hippo Hour Glass", "HEALTHY_GLOVES", "STAT_POTION_AREA_2", "Boss Key"]

        self.shop_costs = ["200", "500", "1000", "1000", "1000"]
        self.min_costs = ["900", "1200", "1700", "1700", "1000"]

        self.selected_item_index = 0  # New attribute to track selected item index
        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Tool Shop Owner.png").convert_alpha()
        self.selected_money_index = 0  # New attribute to track selected item index
        self.stat_point_increase = False
        self.stat_point_increase_index = 0
        self.index_1_bought = False

        self.in_shop = False

    def show_shop(self, state: "GameState"):
        # This method passes the shop items to the textbox
        self.textbox.set_shop_items(self.shop_items, self.shop_costs)
        self.textbox.show_shop_menu = True


    def update(self, state: "GameState"):




        stats = ["Body", "Mind", "Spirit", "Perception", "Luck"]
        # print(self.stat_point_increase)

        if self.stat_point_increase == True:
            state.area2RestScreen.shop_lock = True
            if state.controller.isUpPressed and pygame.time.get_ticks() - self.input_time > 400:
                self.input_time = pygame.time.get_ticks()
                self.stat_point_increase_index = (self.stat_point_increase_index - 1) % len(stats)
                state.controller.isUpPressed = False
                print(self.stat_point_increase_index)

            elif state.controller.isDownPressed and pygame.time.get_ticks() - self.input_time > 400:
                self.input_time = pygame.time.get_ticks()
                self.stat_point_increase_index = (self.stat_point_increase_index + 1) % len(stats)
                state.controller.isDownPressed = False
                print(self.stat_point_increase_index)


            # Handle selection confirmation (e.g., with 'T' press)
            if state.controller.isTPressed and pygame.time.get_ticks() - self.input_time > 400:
                selected_stat = stats[self.stat_point_increase_index]
                print(f"Player selected: {selected_stat}")
                # Handle the logic for applying the stat point increase
                state.controller.isTPressed = False

                if self.stat_point_increase_index == 0 and state.player.body < 2:
                    state.player.body += 1
                    state.player.max_stamina_points += state.player.level_2_body_stamina_increase
                    state.player.stamina_points += state.player.level_2_body_stamina_increase

                    self.stat_point_increase = False
                    state.area2RestScreen.shop_lock = False


                elif self.stat_point_increase_index == 1 and state.player.mind < 2:
                    state.player.mind += 1
                    state.player.max_focus_points += state.player.level_2_mind_focus_increase
                    state.player.focus_points += state.player.level_2_mind_focus_increase
                    Magic.CRAPS_LUCKY_7.add_magic_to_player(state.player, Magic.CRAPS_LUCKY_7)

                    self.stat_point_increase = False
                    state.area2RestScreen.shop_lock = False


                elif self.stat_point_increase_index == 2 and state.player.spirit < 2:
                    state.player.spirit += 1
                    self.stat_point_increase = False
                    state.area2RestScreen.shop_lock = False


                elif self.stat_point_increase_index == 3 and state.player.perception < 2 and Equipment.SOCKS_OF_PERCEPTION.value not in state.player.equipped_items:
                    state.player.perception += 1
                    self.stat_point_increase = False
                    state.area2RestScreen.shop_lock = False


                elif self.stat_point_increase_index == 3 and state.player.perception < 3 and Equipment.SOCKS_OF_PERCEPTION.value in state.player.equipped_items:
                    state.player.perception += 1
                    self.stat_point_increase = False
                    state.area2RestScreen.shop_lock = False


                elif self.stat_point_increase_index == 4 and state.player.luck < 2 and state.player.enhanced_luck == False:
                    state.player.luck += 1
                    self.stat_point_increase = False
                    state.area2RestScreen.shop_lock = False


                elif self.stat_point_increase_index == 4 and state.player.luck < 3 and state.player.enhanced_luck == True:
                    state.player.luck += 1
                    self.stat_point_increase = False
                    state.area2RestScreen.shop_lock = False

        if self.state == "waiting":
            self.update_waiting(state)
            # state.player.canMove = True
        elif self.state == "talking":

            state.player.hide_player = True

            if Equipment.COIN_SAVE_AREA_2.value in state.player.level_two_npc_state:
                self.shop_items[0] = "sold out"

            if Equipment.HIPPO_HOUR_GLASS.value in state.player.quest_items:
                self.shop_items[1] = "sold out"

            if Equipment.HEALTHY_GLOVES.value in state.player.level_two_npc_state:
                self.shop_items[2] = "sold out"

            if Equipment.STAT_POTION_AREA_2.value in state.player.level_two_npc_state:
                self.shop_items[3] = "sold out"

            if Equipment.BOSS_KEY.value in state.player.quest_items:
                self.shop_items[4] = "sold out"



            cost = int(self.shop_costs[self.selected_item_index])


            if state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500 and self.stat_point_increase == False:
                self.input_time = pygame.time.get_ticks()
                self.state = "waiting"
                print("Leaving the shop...")
                self.textbox.reset()
                self.stat_point_increase = False
                self.in_shop = False
                state.player.canMove = True


            if self.textbox.message_index == 0 and self.textbox.is_finished():

                if state.controller.isTPressed:
                    state.controller.isTPressed = False


                    if state.player.money > 899 and self.selected_item_index == 0 and Equipment.COIN_SAVE_AREA_2.value not in state.player.level_two_npc_state:
                        print("HI")
                        self.buy_sound.play()  # Play the sound effect once

                        if state.player.enhanced_luck == True:
                            state.player.luck -= 1
                        Equipment.COIN_SAVE_AREA_2.add_potion_to_player(state.player, Equipment.COIN_SAVE_AREA_2)
                        state.player.money -= 200
                        state.save_game(state.player, state)  # Call the save_game function
                        if state.player.enhanced_luck == True:
                            state.player.luck += 1
                        state.controller.isTPressed = False

                    elif state.player.money < 900 and self.selected_item_index == 0:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                    elif Equipment.COIN_SAVE_AREA_2.value in state.player.level_two_npc_state and self.selected_item_index == 0:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once




                    if state.player.money > 1199 and self.selected_item_index == 1 and Equipment.HIPPO_HOUR_GLASS.value not in state.player.quest_items:
                        print("HIPPOOOOOOOOOOOOOO")
                        self.buy_sound.play()  # Play the sound effect once

                        Equipment.HIPPO_HOUR_GLASS.add_item_to_quest_state(state.player, Equipment.HIPPO_HOUR_GLASS)
                        state.player.money -= 500
                        print(state.player.quest_items)


                    elif state.player.money < 1200 and self.selected_item_index == 1:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                    elif Equipment.HIPPO_HOUR_GLASS.value in state.player.quest_items and self.selected_item_index == 1:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once




                    if state.player.money > 1699 and self.selected_item_index == 2 and Equipment.HEALTHY_GLOVES.value not in state.player.level_two_npc_state:
                        print("HI")
                        self.buy_sound.play()  # Play the sound effect once

                        Equipment.HEALTHY_GLOVES.add_equipment_to_player(state.player, Equipment.HEALTHY_GLOVES)
                        state.player.money -= 1000
                        state.controller.isTPressed = False

                    elif state.player.money < 1700 and self.selected_item_index == 2:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                    elif Equipment.HEALTHY_GLOVES.value in state.player.level_two_npc_state and self.selected_item_index == 2:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once
                    # else:
                    #     print("dsjfl;dsjlafj;jflsajf;j;fja;fkjsda;fjls;ajfl;sjafl;sjal;fjasl;jf;asjf;ls")
                    #     self.cant_buy_sound.play()  # Play the sound effect once


                    if state.player.money > 1699 and self.selected_item_index == 3 and Equipment.STAT_POTION_AREA_2.value not in state.player.level_two_npc_state:
                        print("HI")
                        self.buy_sound.play()  # Play the sound effect once

                        Equipment.STAT_POTION_AREA_2.add_potion_to_player(state.player, Equipment.STAT_POTION_AREA_2)
                        state.player.money -= 1000
                        self.stat_point_increase = True
                        state.controller.isTPressed = False

                    elif state.player.money < 1700 and self.selected_item_index == 3:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                    elif Equipment.STAT_POTION_AREA_2.value in state.player.level_two_npc_state and self.selected_item_index == 3:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once
                    # else:
                    #     print("dsjfl;dsjlafj;jflsajf;j;fja;fkjsda;fjls;ajfl;sjafl;sjal;fjasl;jf;asjf;ls")
                    #     self.cant_buy_sound.play()  # Play the sound effect once




                    if state.player.money > 1001 and self.selected_item_index == 4 and Equipment.BOSS_KEY.value not in state.player.quest_items and Events.ERIKA_IN_PARTY.value in state.player.companions:
                        Equipment.BOSS_KEY.add_item_to_quest_state(state.player, Equipment.BOSS_KEY)
                        state.player.money -= 1000
                        self.buy_sound.play()  # Play the sound effect once
                        state.controller.isTPressed = False

                    elif state.player.money < 1000 and self.selected_item_index == 4:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                    elif Equipment.BOSS_KEY.value in state.player.quest_items and self.selected_item_index == 4:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once

                    elif self.selected_item_index == 4 and Events.ERIKA_IN_PARTY.value not in state.player.companions:
                        state.controller.isTPressed = False
                        self.cant_buy_sound.play()  # Play the sound effect once
                    # else:
                    #     print("dsjfl;dsjlafj;jflsajf;j;fja;fkjsda;fjls;ajfl;sjafl;sjal;fjasl;jf;asjf;ls")
                    #     self.cant_buy_sound.play()  # Play the sound effect once





                if state.controller.isUpPressed and pygame.time.get_ticks() - self.input_time > 400 and self.stat_point_increase == False:
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

                elif state.controller.isDownPressed and pygame.time.get_ticks() - self.input_time > 400 and self.stat_point_increase == False:
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

        # If 'B' is pressed, exit the conversation and allow movement
        if state.controller.isBPressed and pygame.time.get_ticks() - self.input_time > 500:
            self.input_time = pygame.time.get_ticks()
            self.state = "waiting"  # Switch to 'waiting' state
            state.player.canMove = True  # Explicitly set canMove to True when leaving conversation
            self.textbox.reset()  # Reset the textbox
            return

        # If 'T' is pressed and the conversation is finished, exit and allow movement
        if state.controller.isTPressed and self.textbox.is_finished():
            state.controller.isTPressed = False
            self.state = "waiting"  # Switch to 'waiting' state
            state.player.canMove = True  # Explicitly set canMove to True after finishing conversation
            self.textbox.reset()
            return

        # During the conversation, prevent movement
        if self.state == "talking":
            state.player.canMove = False

        # If already in 'waiting' state, ensure player can move
        if self.state == "waiting":
            state.player.canMove = True

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

                if self.selected_item_index == 0 and Equipment.COIN_SAVE_AREA_2.value not in state.player.level_two_npc_state:
                    state.DISPLAY.blit(self.font.render(f"There is only 1 of these on this floor so use it wisely.", True,
                                                        (255, 255, 255)), (70, 460))
                    state.DISPLAY.blit(self.font.render(f"Saves your game.", True,
                                                        (255, 255, 255)), (70, 510))
                if self.selected_item_index == 0 and Equipment.COIN_SAVE_AREA_2.value in state.player.level_two_npc_state:
                    state.DISPLAY.blit(self.font.render(f"Save Coin is Sold out!", True,
                                                        (255, 255, 255)), (70, 460))



                if self.selected_item_index == 1 and Equipment.HIPPO_HOUR_GLASS.value not in state.player.quest_items:
                    state.DISPLAY.blit(self.font.render(f"Increases chance of all swimmers winning ", True,
                                                        (255, 255, 255)), (70, 460))


                    state.DISPLAY.blit(self.font.render(f" This will be always on once bought. ", True,
                                                        (255, 255, 255)), (70, 510))

                elif self.selected_item_index == 1 and Equipment.HIPPO_HOUR_GLASS.value in state.player.quest_items:
                    state.DISPLAY.blit(self.font.render(f"Hippo Hour Glass is sold out! ", True,
                                                        (255, 255, 255)), (70, 460))



                if self.selected_item_index == 2 and Equipment.HEALTHY_GLOVES.value not in state.player.level_two_npc_state:
                    state.DISPLAY.blit(self.font.render(f"Increases stamina by a total of 30 points when equipped! ", True,
                                                        (255, 255, 255)), (70, 460))


                    state.DISPLAY.blit(self.font.render(f"The earlier you buy this the better.", True,
                                                        (255, 255, 255)), (70, 510))

                elif self.selected_item_index == 2 and Equipment.HEALTHY_GLOVES.value in state.player.level_two_npc_state:
                    state.DISPLAY.blit(self.font.render(f"Healthy gloves is sold out! ", True,
                                                        (255, 255, 255)), (70, 460))

                if self.selected_item_index == 3 and Events.STAT_POTION_AREA_2.value not in state.player.level_two_npc_state:
                    state.DISPLAY.blit(self.font.render(f"Adds a stat point of your choice (cannot go past 2). ", True,
                                                        (255, 255, 255)), (70, 460))

                    state.DISPLAY.blit(self.font.render(f"There are only 4 stat points on this level plan carefully ", True,
                                                        (255, 255, 255)), (70, 510))

                elif self.selected_item_index == 3 and Events.STAT_POTION_AREA_2.value in state.player.level_two_npc_state:
                    state.DISPLAY.blit(self.font.render(f"Stat Potion is sold out! ", True,
                                                        (255, 255, 255)), (70, 460))

                if self.selected_item_index == 4 and Equipment.BOSS_KEY.value not in state.player.quest_items:
                    state.DISPLAY.blit(self.font.render(f"The key to allow you to go to boss room. ", True,
                                                        (255, 255, 255)), (70, 460))

                    state.DISPLAY.blit(self.font.render(f"Once you enter boss room there is no turning back. ", True,
                                                        (255, 255, 255)), (70, 510))

                elif self.selected_item_index == 4 and Equipment.BOSS_KEY.value in state.player.quest_items:
                    state.DISPLAY.blit(self.font.render(f"Boss Key is sold out! Good luck! ", True,
                                                        (255, 255, 255)), (70, 460))
                # Handle drawing the shop interaction text

                if self.stat_point_increase == True:
                    # Draw a box on the far right end of the screen, 260 pixels wide and 260 pixels high
                    box_width = 260
                    box_height = 260
                    border_width = 5
                    start_x = state.DISPLAY.get_width() - box_width - 25  # Far right of the screen
                    start_y = state.DISPLAY.get_height() // 2 - box_height // 2 + 10  # Centered vertically

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

                    # Draw the label for maximum stat value
                    state.DISPLAY.blit(self.font.render("Max Value 2:", True, (255, 255, 255)), (start_x + 10, start_y + 20))

                    # Define the list of stats and the vertical position for each
                    stats = ["Body", "Mind", "Spirit", "Perception", "Luck"]
                    stat_values = [
                        state.player.body,
                        state.player.mind,
                        state.player.spirit,
                        state.player.perception - 1 if Equipment.SOCKS_OF_PERCEPTION.value in state.player.equipped_items else state.player.perception,
                        state.player.luck - 1 if state.player.enhanced_luck else state.player.luck,
                    ]

                    # Display the stats names
                    for idx, stat in enumerate(stats):
                        y_position = start_y + 60 + idx * 40  # Adjust vertical spacing
                        state.DISPLAY.blit(self.font.render(stat, True, (255, 255, 255)), (start_x + 60, y_position))

                    # Display the player's current stat values 30 pixels to the right of the stat names
                    for idx, stat_value in enumerate(stat_values):
                        y_position = start_y + 60 + idx * 40  # Adjust vertical spacing
                        state.DISPLAY.blit(self.font.render(str(stat_value), True, (255, 255, 255)), (start_x + 200, y_position))

                    # Draw the arrow next to the currently selected stat based on stat_point_increase_index
                    arrow_y_positions = [60, 100, 140, 180, 220]  # Y positions for the arrow, matching the stats' Y positions
                    arrow_x = start_x + 20  # X position for the arrow
                    arrow_y = start_y + arrow_y_positions[self.stat_point_increase_index]

                    # Draw the arrow ('->') at the current stat's position
                    state.DISPLAY.blit(self.font.render("->", True, (255, 255, 255)), (arrow_x, arrow_y))
