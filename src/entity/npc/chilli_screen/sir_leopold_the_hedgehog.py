import math

import pygame

from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox

##
##sir leopold should block exit till we talk to him post quests
##we will append sir leopold in front of entrance if player has flower
##
##
class SirLeopoldTheHedgeHog(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.textbox = NpcTextBox(
            ["I'm the head hog round these parts and I can use your help!",
             "Oh hero won't you pretty please help my friends, they are hiding out in the hedge maze, I'll reward you real good if you can help. ",
             "Would you like to go now I can show you the way?"],
            (50, 450, 50, 45), 30, 500)
        self.reward_no_hogs = NpcTextBox(
            ["Wow you really suck",
             "Your hopeless.......I guess I have no choice but to join you, by the looks of it you can use a helping paw.Though I'm not giving you coins"],
            (50, 450, 50, 45), 30, 500)
        self.reward_some_hogs = NpcTextBox(
            ["Well at least you tried",
             "Take these 250 coins."],
            (50, 450, 50, 45), 30, 500)
        self.reward_all_hogs = NpcTextBox(
            ["You actually got them all! I was expecting like one or two, maybe 3 tops, but all 4, you are the man!!!",
             "I'll give you 500 coins, it's all that I have. I stole them from the opossum girls.'",
             "Hero: What?",
             "Sir Leopold: Yeah you can say I'm pretty good at stealing. There is something else I need to tell you."],
            (50, 450, 50, 45), 30, 500)

        self.final_message = NpcTextBox(
            ["", "As long as your wearing this I can help you in black jack. (You received sir leopold's paw)" ,
             "Since your Spirit is high I'll join you, the higher spirit you have the more companions will join us",
             "Hero: If I don't hurry up and get to the Doctor I'll be joining the trash cans.",
             "Sir Leopold: Right you are, as for that item I gave you, whenever you hear the 'ting' noise that means I stole something",
             "Hero: Wait you can steal cards? That's allowed?",
             "Sir Leopold: That's right it's allowed as long as your wearing that, rules and all of this place. Welcome to hell as they say, nothing makes sense here.",

             ],
            (50, 450, 50, 45), 30, 500)

        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.to_be_deleted = False  # Flag to mark the object for deletion
        self.textboxstate = "textbox1" # state = "textbox1" | "textbox2" | "textbox3" | "textbox4" | "textbox5"
        self.vanish = False
        self.reward1 = False
        self.reward2 = False
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.t_pressed = False


        self.state_start_time = pygame.time.get_ticks()  # initialize start_time to the current time
        self.state = "waiting"  # states = "waiting" | "talking" | "finished"


        self.character_sprite_image = pygame.image.load(
            "/Users/stevenhalla/code/casino_hell/assets/images/DS DSi - The World Ends With You - Hedge Hado Coa (1).png").convert_alpha()

    def update(self, state: "GameState"):
        # print("YOur hedge hog counter is now at:" + str(state.hedgeMazeScreen.hedge_hog_counter))


        if self.state == "waiting":
            # state.player.canMove = True

            # print("current state is:" + str(self.textboxstate))

            if "blue flower" in state.player.items:
                if state.hedgeMazeScreen.hedge_hog_counter == 0:
                    self.textboxstate = "textbox2"
                    print("no hoggy hogs for u")
                elif state.hedgeMazeScreen.hedge_hog_counter < 4:
                    self.textboxstate = "textbox3"
                elif state.hedgeMazeScreen.hedge_hog_counter == 4:
                    self.textboxstate = "textbox4"



                #     if self.reward_all_hogs.is_finished():
                #         # Transition to textboxstate 5 after reward_all_hogs is finished
                #         self.textboxstate = "textbox5"
                # elif self.textboxstate == "textbox5":
                    # self.final_message.update(state)





            player = state.player

            # print("waiting")
            # if value is below 88 it wont activate for some reason
            min_distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            #
            # if min_distance < 25:
            #     print("nooo")


            self.update_waiting(state)

        elif self.state == "talking":
            state.player.canMove = False

            if self.textbox.is_finished() and "blue flower" not in state.player.items:
                if state.controller.isUpPressed:
                    state.controller.isUpPressed = False

                    self.arrow_index = (self.arrow_index - 1) % len(self.choices)
                    print("Up pressed, arrow_index:", self.arrow_index)  # Debugging line

                elif state.controller.isDownPressed:
                    state.controller.isDownPressed = False

                    self.arrow_index = (self.arrow_index + 1) % len(self.choices)
                    print("Down pressed, arrow_index:", self.arrow_index)  # Debugging line

                if state.controller.isTPressed and self.arrow_index == 0:
                    print("yes")
                    state.player.canMove = True
                    state.chili_area_to_maze_area_entry_point = True

                    state.currentScreen = state.hedgeMazeScreen
                    state.hedgeMazeScreen.start(state)
                    # Handle the selected option
                    selected_option = self.choices[self.arrow_index]
                    print(f"Selected option: {selected_option}")

                else:
                    print("no")
                    state.player.canMove = True



            # self.textbox.reset()
            # self.textbox.message_index = 0
            if self.textbox.message_index == 1:
                if state.controller.isAPressed and \
                        pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    self.state = "waiting"


                elif state.controller.isBPressed and \
                        pygame.time.get_ticks() - self.input_time > 500:
                    self.input_time = pygame.time.get_ticks()
                    print("bye player")
                    self.state = "waiting"

            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        # print(self.state)
        min_distance = math.sqrt(
            (player.collision.x - self.collision.x) ** 2 + (
                        player.collision.y - self.collision.y) ** 2)

        if min_distance < 10:
            print("nooo")

        if state.controller.isTPressed and (
                pygame.time.get_ticks() - self.state_start_time) > 500:
            distance = math.sqrt(
                (player.collision.x - self.collision.x) ** 2 + (
                            player.collision.y - self.collision.y) ** 2)
            # print("distance: " + str(distance))

            if distance < 40:
                # print("start state: talking")
                print("10")

                self.state = "talking"

                self.state_start_time = pygame.time.get_ticks()
                if self.textboxstate == "textbox2":
                    # print("Textbox1")
                    self.reward_no_hogs.reset()
                elif self.textboxstate == "textbox3":
                    # print("Textbox1")
                    self.reward_some_hogs.reset()
                elif self.textboxstate == "textbox4":
                    # print("Textbox1")
                    self.reward_all_hogs.reset()
                elif self.textboxstate == "textbox1":
                    self.textbox.reset()
                elif self.textboxstate == "textbox5":
                    self.final_message.reset()



    def update_talking(self, state: "GameState"):

        current_time = pygame.time.get_ticks()


        if self.textboxstate == "textbox2":
            self.reward_no_hogs.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.reward_no_hogs.is_finished():
                    self.textboxstate = "textbox5"
                    self.state_start_time = current_time
                    self.input_time = current_time  # Update last input time
        elif self.textboxstate == "textbox3":
            self.reward_some_hogs.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.reward_some_hogs.is_finished():
                    state.player.money += 250
                    self.textboxstate = "textbox5"
                    self.state_start_time = current_time
                    self.input_time = current_time
        elif self.textboxstate == "textbox4":
            self.reward_all_hogs.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.reward_all_hogs.is_finished():
                    state.player.money += 500
                    self.textboxstate = "textbox5"
                    self.state_start_time = current_time
                    self.input_time = current_time



        elif self.textboxstate == "textbox1":
            self.textbox.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.textbox.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time
        elif self.textboxstate == "textbox5":
            self.final_message.update(state)
            if state.controller.isTPressed and (current_time - self.input_time > 500):
                if self.final_message.is_finished():
                    self.state = "waiting"
                    self.state_start_time = current_time
                    self.input_time = current_time
                    self.vanish = True
                    state.player.canMove = True

                    if state.player.perception == 0:
                        state.player.items.append("sir leopold's paw")

                        state.player.companions.append("sir leopold")
                        state.player.perception = 1




        if state.controller.isTPressed and self.textbox.is_finished():
            # if state.controller.isTPressed and self.textbox.message_index == 0:
            print("Here we go we're walking here")
            self.menu_index = 0
            self.arrow_index = 0


            # print("start state: waiting")
            # self.textbox.reset()

            self.state = "waiting"
            # if "Nurgle the hedge hog" not in state.player.items:
            #     state.player.items.append("Nurgle the hedge hog")
            #     print("Added: " + str(state.player.items))

            self.state_start_time = pygame.time.get_ticks()
            self.to_be_deleted = True  # Mark the object for deletion

            # self.textbox.reset()

    # def isOverlap(self, entity: "Entity") -> bool:
    #     print("Overlap called")
    #     return self.collision.isOverlap(entity.collision)

    def draw(self, state):
        # rect = (
        # self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        # self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)
        sprite_rect = pygame.Rect(5, 6, 56, 35)

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
            # print("is talking")
            if self.textboxstate == "textbox2":
                self.reward_no_hogs.draw(state)
            elif self.textboxstate == "textbox3":
                self.reward_some_hogs.draw(state)
            elif self.textboxstate == "textbox4":
                self.reward_all_hogs.draw(state)
            elif self.textboxstate == "textbox5":

                self.final_message.draw(state)
            elif self.textboxstate == "textbox1":
                self.textbox.draw(state)

        if self.state == "talking" and "blue flower" not in state.player.items:
            # Draw the "Yes/No" box only on the last message
            if self.textbox.is_finished() and self.textbox.message_at_end():
                bet_box_width = 150
                bet_box_height = 100
                border_width = 5

                screen_width, screen_height = state.DISPLAY.get_size()
                bet_box_x = screen_width - bet_box_width - border_width - 48
                bet_box_y = screen_height - 130 - bet_box_height - border_width - 60

                bet_box = pygame.Surface((bet_box_width, bet_box_height))
                bet_box.fill((0, 0, 0))
                white_border = pygame.Surface((bet_box_width + 2 * border_width, bet_box_height + 2 * border_width))
                white_border.fill((255, 255, 255))
                white_border.blit(bet_box, (border_width, border_width))

                # Calculate text positions
                text_x = bet_box_x + 50 + border_width
                text_y_yes = bet_box_y + 20
                text_y_no = text_y_yes + 40
                # Draw the box on the screen
                state.DISPLAY.blit(white_border, (bet_box_x, bet_box_y))

                # Draw the text on the screen (over the box)
                state.DISPLAY.blit(self.font.render(f"Yes ", True, (255, 255, 255)), (text_x, text_y_yes))
                state.DISPLAY.blit(self.font.render(f"No ", True, (255, 255, 255)), (text_x, text_y_yes + 40))
                arrow_x = text_x - 30  # Adjust the position of the arrow based on your preference
                arrow_y = text_y_yes + self.arrow_index * 40  # Adjust based on the item's height

                # Draw the arrow using pygame's drawing functions (e.g., pygame.draw.polygon)
                # Here's a simple example using a triangle:
                pygame.draw.polygon(state.DISPLAY, (255, 255, 255),
                                    [(arrow_x, arrow_y), (arrow_x - 10, arrow_y + 10), (arrow_x + 10, arrow_y + 10)])
