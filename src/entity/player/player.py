import json
from typing import Tuple

import pygame

from constants import TILE_SIZE, RED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_OFFSET, BLUEBLACK
from entity.entity import Entity


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color: Tuple[int, int, int] = RED
        self.walk_speed = 3.5
        self.money = 2222
        self.image = pygame.image.load(
            "/Users/stevenhalla/code/nfeGame/images/player_walk_0.png")

        # need to put in a max for stamina and focus

        self.exp = 0
        self.inn_badge = False
        self.level = 1
        self.body = 0
        self.mind = 0
        self.spirit = 0
        self.luck = 0
        self.perception = 0
        self.stamina_points = 55
        self.stamina_increase = self.body * 1 * self.level

        self.max_stamina_points = 100 + self.stamina_increase
        self.focus_points = 100
        self.max_focus_points = 100
        self.perks = []
        self.items = []

        self.magicinventory = []
        self.companions = []
        self.canMove = True



        self.hasRabies = False


        self.rabies1time = False
        self.rabiesImmunity = False
        self.level2checker = False
        self.level3checker = False
        self.level4checker = False
        #conflip glasses gives player + 20 gold
        # need ingame menus that explain rules, minues to stamina,and other info
        self.close_status_screen = False

        self.days = 0




    def to_dict(self):
        return {
            "level": self.level,
            "exp": self.exp,
            "stamina_points": self.stamina_points,
            "max_stamina_points": self.max_stamina_points,
            "focus_points": self.focus_points,
            "max_focus_points": self.max_focus_points,
            "companions": self.companions,
            "items": self.items,
            "magicinventory": self.magicinventory,
            "body": self.body,
            "mind": self.mind,
            "spirit": self.spirit,
            "perception": self.perception,
            "luck": self.luck,

            # Add more stats as needed
        }



    def update(self, state: "GameState"):

        controller = state.controller
        controller.update()

        # if controller.isPPressed:
        #     controller.isPPressed = False
        #     self.draw_player_stats(state)

        if controller.isOPressed:
            print("Your inventory for items: " + str(self.items))
            print("Your inventory for magic: " + str(self.magicinventory))
            print("Your body is: " + str(self.body))
            print("Your mind is: " + str(self.mind))
            print("Your spirit is: " + str(self.spirit))
            print("Your luck is: " + str(self.luck))
            print("Your perception is: " + str(self.perception))
            print("Your Hp  is: " + str(self.stamina_points) + "/" + str(self.max_stamina_points))
            print("Your Mp  is: " + str(self.focus_points) + "/" + str(self.max_focus_points))
            print("Your EXP is : " + str(self.exp))
            print("Your Level is : " + str(self.level))
            print("has rabies status: " + str(self.hasRabies))

            controller.isOPressed = False

        if self.exp > 300 and self.level2checker == False and self.level == 2:
            # print("grats you leveld up to level 2")
            self.level = 2
            self.max_stamina_points += 10 + (self.stamina_increase)
            self.max_focus_points += 10
            self.spirit += 1
            self.level2checker = True
            return

        elif self.exp > 500 and self.level3checker == False and self.level == 3:
            # print("grats you leveld up to level 3")
            if "shield" not in self.magicinventory:
                self.magicinventory.append("shield")
                self.max_stamina_points += 10
                self.max_focus_points += 10
                self.level3checker = True
                self.level = 3

                return


        # Define canMove before the for loop
        for npc in state.npcs:
            if npc.isSpeaking:
                self.canMove = False
                break

        if self.canMove:
            if controller.isLeftPressed:
                self.velocity.x = -self.walk_speed
            elif controller.isRightPressed:
                self.velocity.x = self.walk_speed
            else:
                # hard stop
                # self.velocity.x = 0  # default velocity to zero unless key pressed
                # slow stop
                self.velocity.x *= 0.65  # gradually slow the x velocity down
                if abs(self.velocity.x) < 0.15:  # if x velocity is close to zero, just set to zero
                    self.velocity.x = 0

            if controller.isUpPressed:
                self.velocity.y = -self.walk_speed
            elif controller.isDownPressed:
                self.velocity.y = self.walk_speed
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



        # for npc in state.npcs:
        #     # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
        #     if self.collision.isOverlap(npc.collision) or self.isOutOfBounds():
        #         print("collide with npc: " + str(npc.collision.toTuple()))
        #         self.undoLastMove()
        #         break

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
                print("collide with npc: " + str(demon.collision.toTuple()))
                self.undoLastMove()
                break

        ###
        ### DO NOT DELETE ANY OF THIS CODE, THIS IS FOR SCREEN BOUNDRYS SOMETHING IS WRONG WITH MY
        ### BOX I'LL HAVE TO GET KENNY HELP LATER
        ###

        # for treasurechests in state.treasurechests:
        #     # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
        #     if self.collision.isOverlap(treasurechests.collision) or self.isOutOfBounds():
        #         print("collide with chests: " + str(treasurechests.collision.toTuple()))
        #         self.undoLastMove()
        #         break
        #
        # for demon in state.demons:
        #     # print("p(" + str(state.player.collision.x) + "," + str(state.player.collision.x) + "),n(" + str(npc.collision.x) + "," + str(npc.collision.x) + ")")
        #     if self.collision.isOverlap(
        #             demon.collision) or self.isOutOfBounds():
        #         print("collide with npc: " + str(demon.collision.toTuple()))
        #         self.undoLastMove()
        #         break

        # if controller.isQPressed:
        #     state.currentScreen = state.coinFlipScreen
        #     state.coinFlipScreen.start(state)
        #
        # elif controller.isPPressed:
        #     state.currentScreen = state.opossumInACanScreen
        #     state.opossumInACanScreen.start(state)

    # def isOutOfBounds(self) -> bool:
    #     return self.collision.x + self.collision.width > SCREEN_WIDTH or self.collision.x < 0 or self.collision.y + self.collision.height > SCREEN_HEIGHT or self.collision.y < 0

    def draw(self, state):
        # Get the current dimensions of the image
        original_width, original_height = self.image.get_size()

        # Calculate the new dimensions of the image
        new_width = original_width * 1.7
        new_height = original_height * 1.7

        # Scale the image
        scaled_image = pygame.transform.scale(self.image,
                                              (new_width, new_height))

        # Calculate the center of the image
        image_center_x = new_width // 2
        image_center_y = new_height // 2

        # Define an offset that will be used to draw the image at the center of the player
        # offset_x = self.collision.x + self.collision.width // 2 - image_center_x
        # offset_y = self.collision.y + self.collision.height // 2 - image_center_y

        # Draw the image on the display surface
        state.DISPLAY.blit(scaled_image, PLAYER_OFFSET)

    def draw_player_stats(self, state):
        # Create a black surface of size 600x600
        stats_surface = pygame.Surface((580, 580))
        state.DISPLAY.fill(BLUEBLACK)

        # Set the font for the text
        font = pygame.font.Font(None, 36)

        # Define the stats to display
        stats = [
            f"Level: {self.level}",
            f"Exp: {self.exp}",
            f"Stamina: {self.stamina_points}" + "/" f"{self.max_stamina_points}",
            f"Magic Points: {self.focus_points}" + "/" f"{self.max_focus_points}",
            f"Companions: {self.companions}",
            f"Items: {self.items}",
            f"Magic spells: {self.magicinventory}",
            f"Body: {self.body}",
            f"Mind: {self.mind}",
            f"Spirit: {self.spirit}",
            f"Perception: {self.perception}",
            f"Luck: {self.luck}",
            f"Day: {self.days}",
            f"Press L to Load",

            # Add more stats as needed
        ]

        # Draw each stat on the stats_surface
        for i, stat in enumerate(stats):
            text = font.render(stat, True, (255, 255, 255))  # White color for the text
            stats_surface.blit(text, (50, 30 + i * 40))  # Adjust the position as needed

        # You can adjust these values to position the box as you like
        box_x = SCREEN_WIDTH / 2 - 300  # Center the box in the middle of the screen width
        box_y = SCREEN_HEIGHT / 2 - 290  # Center the box in the middle of the screen height

        # Display the stats surface on the main display
        state.DISPLAY.blit(stats_surface, (box_x, box_y))

        border_color = (255, 255, 255)  # White color
        border_rect = pygame.Rect(box_x, box_y, 580, 580)  # The rectangle that represents the border
        border_thickness = 5  # Adjust the thickness as needed
        pygame.draw.rect(state.DISPLAY, border_color, border_rect, border_thickness)

        if state.controller.isLPressed:
            state.controller.isLPressed = False
            print("L is pressed")
            # Call the load_game function when the L key is pressed
            self.load_game(state)

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
            state.player.level = player_data['level']
            state.player.exp = player_data['exp']
            state.player.stamina_points = player_data['stamina_points']
            state.player.max_stamina_points = player_data['max_stamina_points']
            state.player.focus_points = player_data['focus_points']
            state.player.max_focus_points = player_data['max_focus_points']
            state.player.companions = player_data['companions']
            state.player.items = player_data['items']
            state.player.magicinventory = player_data['magicinventory']
            state.player.body = player_data['body']
            state.player.mind = player_data['mind']
            state.player.spirit = player_data['spirit']
            state.player.perception = player_data['perception']
            state.player.luck = player_data['luck']

            innkeeper_position_x = 16 * 22
            innkeeper_position_y = 16 * 11
            state.player.setPosition(innkeeper_position_x, innkeeper_position_y)

            # Switch to the restScreen
            state.currentScreen = state.restScreen
            state.restScreen.start(state)
            # ... more stats as needed

            print("Game loaded successfully.")

        except Exception as e:
            print(f"Failed to load game: {e}")





