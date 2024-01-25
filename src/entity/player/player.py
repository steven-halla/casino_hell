from typing import Tuple

import pygame

from constants import TILE_SIZE, RED, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_OFFSET
from entity.entity import Entity


class Player(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color: Tuple[int, int, int] = RED
        self.walk_speed = 3.5
        self.money = 1500
        self.image = pygame.image.load(
            "/Users/stevenhalla/code/nfeGame/images/player_walk_0.png")

        # need to put in a max for stamina and focus
        self.stamina_points = 90
        self.max_stamina_points = 100

        self.focus_points = 90
        self.max_focus_points = 100
        self.exp = 0
        self.inn_badge = False
        self.level = 1
        self.body = 0
        self.mind = 0
        self.spirit = 0
        self.luck = 0
        self.perception = 0
        self.perks = []
        self.items = ["coin flip glasses"]
        self.magicinventory = []
        self.canMove = True
        self.hasRabies = False
        self.rabies1time = False
        self.rabiesImmunity = False
        #conflip glasses gives player + 20 gold
        # need ingame menus that explain rules, minues to stamina,and other info


    def update(self, state: "GameState"):
        controller = state.controller
        controller.update()

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
            print("has rabies status: " + str(self.hasRabies))

            controller.isOPressed = False

        if self.exp > 1000:
            print("grats you leveld up to level 2")
            self.level = 2

        if self.exp >= 3000:
            self.level = 3
            print(self.exp)
            if self.exp > 3000:
                self.exp = 3000


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
                print("collide with npc: " + str(npc.collision.toTuple()))
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
