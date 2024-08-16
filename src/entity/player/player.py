import json
from typing import Tuple

import pygame

from constants import TILE_SIZE, RED, SCREEN_WIDTH, SCREEN_HEIGHT, BLUEBLACK
from entity.entity import Entity


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color: Tuple[int, int, int] = RED
        self.walk_speed = 3.5
        self.money = 1000
        self.current_frame_index = 0
        self.exp = 0
        self.inn_badge = False
        self.level = 1
        self.body = 0
        self.mind = 0
        self.spirit = 0
        self.luck = 0
        self.food = 0
        self.perception = 2
        self.stamina_points = 160
        self.stamina_increase = self.body * 1 * self.level
        self.stamina_guard = False
        self.max_stamina_points = 160 + self.stamina_increase
        self.focus_points = 55
        self.max_focus_points = 10
        self.perks = []
        self.items = ["sir leopold's paw"]
        self.npc_items = []
        self.magicinventory = ["shield",  "shake" ]
        self.companions = []
        self.canMove = True
        self.level3janetreward = False
        self.hasRabies = False
        self.rabies1time = False
        self.rabiesImmunity = False
        self.level2checker = False
        self.level3checker = False
        self.level4checker = False
        self.level5checker = False
        self.level6checker = False
        self.close_status_screen = False
        self.days = 0
        self.isBossWorthy = False
        self.realBarKeep = False
        self.shop_keep_potion = False
        self.shop_keep_save_coin = False
        self.current_frame_index = 0  # Current index in the sprite list
        # Timer for sprite animation
        self.sprite_animation_timer = 0
        self.sprite_animation_interval = 500  # 500 milliseconds (0.5 seconds) per frame
        self.left_animation_frames = []  # Holds frames for left movement animation
        # Initialize pygame's clock to manage the animation timer
        self.clock = pygame.time.Clock()
        # TODO refrence the images with relative paths
        self.up_sprite = pygame.image.load('/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Jack.png').convert_alpha()
        self.down_sprite = pygame.image.load('/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Jack.png').convert_alpha()
        self.left_sprite = pygame.image.load('/Users/stevenhalla/code/casino_hell/assets/images/SNES - Harvest Moon - Jack.png').convert_alpha()
        self.left_frames = [(28, 146, 18, 26), (46, 146, 18, 26), (63, 146, 17.9, 26)]
        self.down_frames = [(28, 120, 18, 26), (45, 120, 18, 26), (63, 120, 17.9, 26)]
        self.up_frames = [(29, 172, 18, 26), (47, 172, 18, 26), (64, 172, 17.9, 26)]
        # Set the initial direction and frame index.
        self.current_direction = 'down'  # Default direction
        self.music_file = "/Users/stevenhalla/code/casino_hell/assets/music/levelup.mp3"
        self.music_volume = 0.5  # Adjust as needed
        self.level_two_npc_state = []
        self.leveling_up = False

        self.stamina_increase_from_level = 0
        self.focus_increase_from_level = 0
        self.stat_point_increase = False
        self.menu_index = 0
        self.menu_paused = False

    def to_dict(self, state: "GameState") -> dict:
        return {
            "level": self.level,
            "exp": self.exp,
            "stamina_points": self.stamina_points,
            "max_stamina_points": self.max_stamina_points,
            "focus_points": self.focus_points,
            "max_focus_points": self.max_focus_points,
            "companions": self.companions,
            "items": self.items,
            "npcitems": self.npc_items,
            "magicinventory": self.magicinventory,
            "body": self.body,
            "mind": self.mind,
            "spirit": self.spirit,
            "perception": self.perception,
            "luck": self.luck,
            "money": self.money,
            "rabies": self.hasRabies,
            "immunity": self.rabiesImmunity,
            "level3reward": self.level3janetreward,
            "food": self.food,
            "days": self.days,
            "leveltwonpcstate": self.level_two_npc_state,

            "cutscene1": state.restScreen.barscene1,
            "cutscene2": state.restScreen.barscene2,

            "quest1complete": state.gamblingAreaScreen.five_hundred_opossums,

            "coinfliptedmoney": state.coinFlipTedScreen.coinFlipTedMoney,
            "coinflipfredmoney": state.coinFlipFredScreen.coinFlipFredMoney,

            "opossumnellymoney": state.opossumInACanNellyScreen.nellyOpossumMoney,
            "opossumsallymoney": state.opossumInACanSallyScreen.sallyOpossumMoney,

            "blackjackthomasmoney": state.blackJackThomasScreen.cheater_bob_money,
            "blackjackrumblebillmoney": state.blackJackRumbleBillScreen.cheater_bob_money,

            "shopkeeperpotion": self.shop_keep_potion,
            "shopkeepersavecoin": self.shop_keep_save_coin,


            # level 2
            "slotsrippasnappamoney": state.slotsRippaSnappaScreen.money,

            # Add more stats as needed
        }


    def update(self, state: "GameState"):
        if state.controller.isAPressed:

            print("Your nPc inventory issss:::   " + str(state.player.npc_items))
            print("Your level 2 NPC state  issss:::   " + str(state.player.level_two_npc_state))



        controller = state.controller
        controller.update()


        if self.exp >= 100 and self.level2checker == False:
            print("grats you leveld up to level 2")
            self.level = 2

            if self.spirit < 1:
                self.max_stamina_points += 10 + (self.stamina_increase)
                self.max_focus_points += 10
                self.spirit += 1
            self.level2checker = True
            self.leveling_up = True
            return

        if self.exp >= 300 and self.level3checker == False:
            print("grats you leveld up to level 3")
            # if "shield" not in self.magicinventory:
            if "shield" not in state.player.magicinventory:
                self.magicinventory.append("shield")
                self.max_stamina_points += 10
                self.max_focus_points += 10
            self.level3checker = True
            self.leveling_up = True

            self.level = 3

            return

        if self.exp >= 600 and self.level4checker == False:
            print("grats you leveld up to level 4")
            if "level 4 token" not in state.player.npc_items:
            # if "shield" not in self.magicinventory:
                state.player.npc_items.append("level 4 token")
                # TODO, DO THIS! NOT RAW STRING
                # state.player.npc_items.append(Events.LEVEL_4_TOKEN)
                self.max_stamina_points += 20
                self.max_focus_points += 20
            self.level4checker = True
            self.level = 4
            self.leveling_up = True


            return

        if self.exp >= 1200 and self.level5checker == False:
            print("grats you leveld up to level 5")
            if "level 5 token" not in state.player.npc_items:
                # if "shield" not in self.magicinventory:
                state.player.npc_items.append("level 4 token")
                # TODO, DO THIS! NOT RAW STRING
                # state.player.npc_items.append(Events.LEVEL_4_TOKEN)
                stamina_increase = 20
                self.max_stamina_points += stamina_increase
                self.stamina_increase_from_level = stamina_increase

                focus_increase = 20
                self.max_focus_points += focus_increase
                self.focus_increase_from_level = focus_increase
                self.stat_point_increase = True


            self.level5checker = True
            self.level = 5
            self.leveling_up = True


            return

        if self.exp >= 2000 and self.level6checker == False:
            print("grats you leveld up to level 6")
            if "level 6 token" not in state.player.npc_items:
                # if "shield" not in self.magicinventory:
                state.player.npc_items.append("level 4 token")
                # TODO, DO THIS! NOT RAW STRING
                # state.player.npc_items.append(Events.LEVEL_4_TOKEN)
                self.max_stamina_points += 20
                self.max_focus_points += 20
            self.level6checker = True
            self.level = 6
            self.leveling_up = True


            return


        # Define canMove before the for loop
        for npc in state.npcs:
            if npc.isSpeaking:
                self.canMove = False
                break

        if self.canMove:
            if controller.isLeftPressed:
                self.velocity.x = -self.walk_speed
                self.current_direction = 'left'
                current_time = pygame.time.get_ticks()

                # Check if it's time to update to the next frame based on the interval
                if (current_time - self.sprite_animation_timer) > self.sprite_animation_interval:
                    self.sprite_animation_timer = current_time  # Reset the timer for the next frame update

                    # Update the frame index, looping back to 0 if at the end of the list
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.left_frames)

            elif controller.isRightPressed:
                self.velocity.x = self.walk_speed
                self.current_direction = 'right'
                current_time = pygame.time.get_ticks()

                # Check if it's time to update to the next frame based on the interval
                if (current_time - self.sprite_animation_timer) > self.sprite_animation_interval:
                    self.sprite_animation_timer = current_time  # Reset the timer for the next frame update

                    # Update the frame index, looping back to 0 if at the end of the list
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.left_frames)

            else:
                # hard stop
                # self.velocity.x = 0  # default velocity to zero unless key pressed
                # slow stop
                self.velocity.x *= 0.65  # gradually slow the x velocity down
                if abs(self.velocity.x) < 0.15:  # if x velocity is close to zero, just set to zero
                    self.velocity.x = 0

            if controller.isUpPressed:
                self.velocity.y = -self.walk_speed
                self.current_direction = 'up'
                current_time = pygame.time.get_ticks()

                # Check if it's time to update to the next frame based on the interval
                if (current_time - self.sprite_animation_timer) > self.sprite_animation_interval:
                    self.sprite_animation_timer = current_time  # Reset the timer for the next frame update

                    # Update the frame index, looping back to 0 if at the end of the list
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.up_frames)


            elif controller.isDownPressed:
                self.velocity.y = self.walk_speed
                self.current_direction = 'down'
                current_time = pygame.time.get_ticks()

                # Check if it's time to update to the next frame based on the interval
                if (current_time - self.sprite_animation_timer) > self.sprite_animation_interval:
                    self.sprite_animation_timer = current_time  # Reset the timer for the next frame update

                    # Update the frame index, looping back to 0 if at the end of the list
                    self.current_frame_index = (self.current_frame_index + 1) % len(self.down_frames)

            else:
                # hard stop
                # self.velocity.y = 0  # default velocity to zero unless key pressed
                # slow stop
                self.velocity.y *= 0.65  # gradually slow the y velocity down
                if abs(self.velocity.y) < 0.15:  # if y velocity is close to zero, just set to zero
                    self.velocity.y = 0

        else:  # if can not move, set velocity to zero
            self.velocity.x = 0
            self.velocity.y = 0

        # move player by velocity
        # note that if we have any collisions later we will undo the movements.
        # TODO test collision BEFORE moving
        self.setPosition(self.position.x + self.velocity.x,
                         self.position.y + self.velocity.y)



        if self.isOverlap(state.obstacle):
            self.undoLastMove()




        for npc in state.npcs:
            # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
            if self.collision.isOverlap(npc.collision) :



                # print("collide with npc: " + str(npc.collision.toTuple()))
                # print("moogle pants")

                self.undoLastMove()
                break

        for treasurechests in state.treasurechests:
            # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
            if self.collision.isOverlap(treasurechests.collision) :
                print("collide with chests: " + str(treasurechests.collision.toTuple()))
                self.undoLastMove()
                break

        for demon in state.demons:
            # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
            if self.collision.isOverlap(
                    demon.collision) :
                # print("collide with npc: " + str(demon.collision.toTuple()))
                self.undoLastMove()
                break


    def draw(self, state):
        sprite = None  # Initialize sprite to None

        if self.current_direction == 'up':
            # Define the rectangle for the up sprite
            frame_rect = self.up_frames[self.current_frame_index]

            # Create a pygame.Rect object from the frame_rect tuple
            sprite_rect = pygame.Rect(*frame_rect)

            # Use subsurface to get the specific frame from the sprite sheet
            current_frame_sprite = self.up_sprite.subsurface(sprite_rect)

            # Calculate the position to draw the sprite (adjust as necessary for your game's coordinates)
            sprite_x = self.position.x
            sprite_y = self.position.y
            sprite = self.up_sprite.subsurface(sprite_rect)

            # Draw the current frame to the screen
            # state.DISPLAY.blit(current_frame_sprite, (sprite_x, sprite_y))
        elif self.current_direction == 'down':
            frame_rect = self.down_frames[self.current_frame_index]

            # Create a pygame.Rect object from the frame_rect tuple
            sprite_rect = pygame.Rect(*frame_rect)

            # Use subsurface to get the specific frame from the sprite sheet
            current_frame_sprite = self.down_sprite.subsurface(sprite_rect)

            # Calculate the position to draw the sprite (adjust as necessary for your game's coordinates)
            sprite_x = self.position.x
            sprite_y = self.position.y
            sprite = self.left_sprite.subsurface(sprite_rect)

            # Draw the current frame to the screen
            # state.DISPLAY.blit(current_frame_sprite, (sprite_x, sprite_y))
            # Define the rectangle for the down sprite
            # sprite_rect = pygame.Rect(22, 120, 24, 26)  # Your provided values for the 'down' sprite
            # sprite = self.down_sprite.subsurface(sprite_rect)

        if self.current_direction == 'left':
            # Get the current frame rectangle based on self.current_frame_index
            frame_rect = self.left_frames[self.current_frame_index]

            # Create a pygame.Rect object from the frame_rect tuple
            sprite_rect = pygame.Rect(*frame_rect)

            # Use subsurface to get the specific frame from the sprite sheet
            current_frame_sprite = self.left_sprite.subsurface(sprite_rect)

            # Calculate the position to draw the sprite (adjust as necessary for your game's coordinates)
            sprite_x = self.position.x
            sprite_y = self.position.y
            sprite = self.left_sprite.subsurface(sprite_rect)

            # Draw the current frame to the screen
            # state.DISPLAY.blit(current_frame_sprite, (sprite_x, sprite_y))

        elif self.current_direction == 'right':
            frame_rect = self.left_frames[self.current_frame_index]

            # Create a pygame.Rect object from the frame_rect tuple
            sprite_rect = pygame.Rect(*frame_rect)

            # Use subsurface to get the specific frame from the sprite sheet
            current_frame_sprite = self.left_sprite.subsurface(sprite_rect)
            current_frame_sprite = pygame.transform.flip(current_frame_sprite, True, False)

            # Scale the selected sprite
            scaled_sprite = pygame.transform.scale(current_frame_sprite, (50, 50))

            # Assign the scaled sprite to the sprite variable
            sprite = scaled_sprite

            # Calculate the position to draw the sprite, adjusting for the camera
            sprite_x = self.collision.x + state.camera.x - 10
            sprite_y = self.collision.y + state.camera.y - 10

            # Draw the sprite on the screen
            # state.DISPLAY.blit(sprite, (sprite_x, sprite_y))

            # Scale the selected sprite
        scaled_sprite = pygame.transform.scale(sprite, (50, 50))

        # Calculate the position to draw the sprite, adjusting for the camera
        sprite_x = self.collision.x + state.camera.x - 10
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the sprite on the screen
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

    def draw_player_stats(self, state):
        self.menu_paused = True

        # Get the dimensions of the display
        screen_width = state.DISPLAY.get_width()
        screen_height = state.DISPLAY.get_height()

        # 1. Black Background
        state.DISPLAY.fill((0, 0, 0))  # Fill the entire screen with black

        # 2. Second Box (Main Menu Area)
        main_box_width = screen_width - 20  # 10 pixels padding on both sides
        main_box_height = screen_height - 20  # 10 pixels padding on top and bottom
        main_box = pygame.Surface((main_box_width, main_box_height))

        # Define the gradient colors (top to bottom)
        top_color = (0, 0, 139)  # Dark blue
        bottom_color = (135, 206, 250)  # Light blue

        # Apply the gradient to the main box surface
        for y in range(main_box_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // main_box_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // main_box_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // main_box_height,
            )
            pygame.draw.line(main_box, color, (0, y), (main_box_width, y))

        # Draw the main box centered on the screen
        state.DISPLAY.blit(main_box, (10, 10))

        # Add a white border around the main box
        border_thickness = 3
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(10, 10, main_box_width, main_box_height), border_thickness)

        # 3. Third Box (Top right box)
        third_box_width = 220
        third_box_height = 400
        third_box = pygame.Surface((third_box_width, third_box_height))

        # Apply the same gradient or different one to the third box
        for y in range(third_box_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // third_box_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // third_box_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // third_box_height,
            )
            pygame.draw.line(third_box, color, (0, y), (third_box_width, y))

        # Position the third box on the right side of the screen
        third_box_x = screen_width - third_box_width - 10  # 10 pixels padding from the right
        third_box_y = 10  # 10 pixels padding from the top
        state.DISPLAY.blit(third_box, (third_box_x, third_box_y))

        # Add a border to the third box
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(third_box_x, third_box_y, third_box_width, third_box_height), border_thickness)

        # 4. Fourth Box (Bottom right box)
        fourth_box_width = 220
        fourth_box_height = 100
        fourth_box = pygame.Surface((fourth_box_width, fourth_box_height))

        # Apply the gradient to the fourth box
        for y in range(fourth_box_height):
            color = (
                bottom_color[0] + (top_color[0] - bottom_color[0]) * y // fourth_box_height,
                bottom_color[1] + (top_color[1] - bottom_color[1]) * y // fourth_box_height,
                bottom_color[2] + (top_color[2] - bottom_color[2]) * y // fourth_box_height,
            )
            pygame.draw.line(fourth_box, color, (0, y), (fourth_box_width, y))

        # Position the fourth box below the third box
        fourth_box_x = screen_width - fourth_box_width - 10  # 10 pixels padding from the right
        fourth_box_y = third_box_y + third_box_height + 10  # 10 pixels padding below the third box
        state.DISPLAY.blit(fourth_box, (fourth_box_x, fourth_box_y))

        # Add a border to the fourth box
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(fourth_box_x, fourth_box_y, fourth_box_width, fourth_box_height), border_thickness)

        # Render the menu items and arrow in the third box

        # Set the font for the menu items
        font = pygame.font.Font(None, 36)  # You can adjust the font size as needed

        # Define the menu items
        menu_items = ["Equipment", "Quest Items", "Magic", "Status", "Companions"]

        # Starting y position for the first item
        item_y = 30  # Adjust this as needed to center vertically within the box

        # Draw each menu item in the box with 20 pixels between each
        for item in menu_items:
            text_surface = font.render(item, True, (255, 255, 255))  # White color for text
            third_box.blit(text_surface, (50, item_y))  # Adjust x-position as needed
            item_y += text_surface.get_height() + 20  # Move to the next line with 20 pixels spacing

        # Define the arrow symbol
        arrow = "->"

        # Render the arrow
        arrow_surface = font.render(arrow, True, (255, 255, 255))  # White color for the arrow

        # Calculate the y position of the arrow based on the menu index
        arrow_y = 28 + self.menu_index * (text_surface.get_height() + 20)

        # Draw the arrow in the top box, aligned with the menu item
        third_box.blit(arrow_surface, (10, arrow_y))  # Positioned 20 pixels from the left edge

        # Set the font for the text in the fourth box
        font = pygame.font.Font(None, 36)  # You can adjust the font size as needed

        # Create the text to display in the fourth box
        gold_text = f"GP"

        # Set the x and y positions, similar to the top box
        text_surface = font.render(gold_text, True, (255, 255, 255))  # White color for text
        fourth_box.blit(text_surface, (30, 30))  # 30 pixels from the left edge and top

        money_text = f"{self.money}"

        # Set the x and y positions, similar to the top box
        text_surface = font.render(money_text, True, (255, 255, 255))  # White color for text
        fourth_box.blit(text_surface, (75, 50))  # 30 pixels from the left edge and top

        # Display everything on the screen
        state.DISPLAY.blit(third_box, (third_box_x, third_box_y))
        state.DISPLAY.blit(fourth_box, (fourth_box_x, fourth_box_y))

        # Draw the borders around each box
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(third_box_x, third_box_y, third_box_width, third_box_height), border_thickness)
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), pygame.Rect(fourth_box_x, fourth_box_y, fourth_box_width, fourth_box_height), border_thickness)

        # Handle menu navigation with up/down arrow keys
        if self.menu_paused:
            if state.controller.isUpPressed:
                self.menu_index = (self.menu_index - 1) % len(menu_items)
                state.controller.isUpPressed = False

            elif state.controller.isDownPressed:
                self.menu_index = (self.menu_index + 1) % len(menu_items)
                state.controller.isDownPressed = False

    def load_game(self, state):

        # Define the file path
        file_path = '/Users/stevenhalla/code/casino_hell/assets/save_data.json'

        # Read the JSON string from the file
        try:
            with open(file_path, 'r') as file:
                player_data_json = file.read()

            # Convert JSON string to a dictionary
            player_data = json.loads(player_data_json)


            # Update player's stats with the loaded data
            state.player.level_two_npc_state = player_data['leveltwonpcstate']

            state.player.level = player_data['level']
            state.player.exp = player_data['exp']
            state.player.stamina_points = player_data['stamina_points']
            state.player.max_stamina_points = player_data['max_stamina_points']
            state.player.focus_points = player_data['focus_points']
            state.player.max_focus_points = player_data['max_focus_points']
            state.player.companions = player_data['companions']
            state.player.items = player_data['items']
            state.player.npc_items = player_data['npcitems']
            state.player.magicinventory = player_data['magicinventory']
            state.player.body = player_data['body']
            state.player.mind = player_data['mind']
            state.player.spirit = player_data['spirit']
            state.player.perception = player_data['perception']
            state.player.luck = player_data['luck']
            state.player.money = player_data['money']
            state.player.hasRabies = player_data['rabies']
            state.player.rabiesImmunity = player_data['immunity']
            state.player.level3janetreward = player_data['level3reward']
            state.player.food = player_data['food']
            state.player.days = player_data['days']
            state.restScreen.barscene1 = player_data['cutscene1']
            state.restScreen.barscene2 = player_data['cutscene2']
            state.gamblingAreaScreen.five_hundred_opossums = player_data['quest1complete']
            state.coinFlipTedScreen.coinFlipTedMoney = player_data['coinfliptedmoney']
            state.coinFlipFredScreen.coinFlipFredMoney = player_data['coinflipfredmoney']
            state.opossumInACanNellyScreen.nellyOpossumMoney = player_data['opossumnellymoney']
            state.opossumInACanSallyScreen.sallyOpossumMoney = player_data['opossumsallymoney']
            state.blackJackThomasScreen.cheater_bob_money = player_data['blackjackthomasmoney']
            state.blackJackRumbleBillScreen.cheater_bob_money = player_data['blackjackrumblebillmoney']

            state.player.shop_keep_potion = player_data['shopkeeperpotion']
            state.player.shop_keep_save_coin = player_data['shopkeepersavecoin']


            #level 2

            state.slotsRippaSnappaScreen.money = player_data['slotsrippasnappamoney']





            innkeeper_position_x = 16 * 22
            innkeeper_position_y = 16 * 11
            state.player.setPosition(innkeeper_position_x, innkeeper_position_y)

            # Switch to the restScreen
            # state.currentScreen = state.restScreen
            state.currentScreen = state.area2RestScreen


            state.area2RestScreen.start(state)
            # ... more stats as needed

            print("Game loaded successfully.")

        except Exception as e:
            print(f"Failed to load game: {e}")
