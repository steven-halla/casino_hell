

import math
import pygame


from entity.npc.npc import Npc
from entity.gui.textbox.npc_text_box import NpcTextBox
from game_constants.events import Events
from game_constants.magic import Magic


# in order to get this quest to work:
# if you win 500 coins get a coin
# if you win 500 coins from two games those coins become mega coin.
# if you rest at the innn, the lower coins vanish , but an inn stay wont eras the mega coin
class ErikaBoss(Npc):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

        # Integrated textbox content into guy_messages
        self.selected_item_index = 0
        self.black_jack_thomas_messages = {
            "welcome_message": NpcTextBox(
                ["Erika:Tadaaa! Are you surprised? Yeah I'm the boss....what kind of deal were you wanting to make? I already know what I want when you lose.",

                "Hero: Well this was unexpected... I was going to ask to vacate all the rib demons but I have a new plan.",
                 "Sir Leopold: Awwwwww, see, I knew you had a good heart.",

                "Erika: Oh you are so bold Hero. Very easy to tell what you're thinking, not that I blame you after seeing my real form.",
                "Hero: No, not that. If I win, i want you to contiue traveling with us, and to never betray our party going forward.",
                "Sir Leopold: Having a demon on our team would give us some advantages, good thinking!",
                "Erika: You still dont' want to eat me, so disapointing. I wasn't expecting you to ask for that...Ok I agree to your terms, but if I win...",
                "You have to be my slave, forever. I'm going to make you do so many horrible things for me ho ho ho, you'll become my play-thing.",
                "Hero: I accept your terms, if thats all I'm ready to battle if you are.",
                "Erika: Wait, thats it, do you have ANY idea of all the horrible things I'll do to you, it's not going to be fun.",
                "I mean it'll be fun for me, but you'll be hating your new existance, you're going to be begging me for mercy, and I never ever grant mercy tee hee.",
                "You can still change your mind, we can continue on like nothing ever happened, pretty please? With chicken nuggies on top?",
                "Hero: Sorry Erika, if you're the boss then were fighting, it's as simple as that. No way you're escaping it.",
                "Sir Leopold: Damn, maybe she's right? Maybe reconsider things? She's going to be stronger than the last floor boss and he was pretty tough.",
                "Hero: None of that matters, it's irrelevant, not like she's going to win, this is a freeby as far as I'm concerned.",
                "Erika: Freeby? You must really think that I'm going to take it easy on you, I have my demon pride 'hero'.",
                "The time for talk is over... I tried to warn you hero, you dum dum stupid idiot head. You're going to regret fighting me, pathetic human scum!",


                 ],
                (50, 450, 700, 130), 36, 500),
            "defeated_message": NpcTextBox(
                ["That's the 100th time I've lost, I don't know why the demons keep giving me coins."],
                (50, 450, 700, 130), 36, 500),

            "rabies_message": NpcTextBox(
                ["GET AWAY FROM ME YOU FROTHY MOUTHED BASTARD."],
                (50, 450, 700, 130), 36, 500),

        }
        self.choices = ["Yes", "No"]
        self.menu_index = 0
        self.input_time = pygame.time.get_ticks()
        self.state_start_time = pygame.time.get_ticks()
        self.state = "waiting"
        self.black_jack_thomas_defeated = False
        self.font = pygame.font.Font(None, 36)
        self.arrow_index = 0  # Initialize the arrow index to the first item (e.g., "Yes")
        self.t_pressed = False
        self.screen_black = False

        self.character_sprite_image = pygame.image.load(
            "./assets/images/erika_demon_sprites.png").convert_alpha()

    def update(self, state: "GameState"):
        if self.state == "waiting":
            self.update_waiting(state)
        elif self.state == "talking":
            self.update_talking(state)

    def update_waiting(self, state: "GameState"):
        player = state.player
        distance = math.sqrt((player.collision.x - self.collision.x) ** 2 +
                             (player.collision.y - self.collision.y) ** 2)

        if distance < 40 and state.controller.isTPressed and \
                (pygame.time.get_ticks() - self.state_start_time) > 500 and state.player.menu_paused == False:
            self.state = "talking"
            self.state_start_time = pygame.time.get_ticks()


            self.black_jack_thomas_messages["welcome_message"].reset()

    def update_talking(self, state: "GameState"):
        current_message = (
            self.black_jack_thomas_messages["welcome_message"]
            if state.player.hasRabies
            else (
                self.black_jack_thomas_messages["welcome_message"]

            )
        )
        current_message.update(state)

        # Lock the player in place while talking
        state.player.canMove = False

        # Check for keypresses only once per frame
        if current_message.is_finished() and current_message.message_at_end():

            if state.controller.isUpPressed:
                self.arrow_index = (self.arrow_index - 1) % len(self.choices)
                state.controller.isUpPressed = False


            elif state.controller.isDownPressed:
                self.arrow_index = (self.arrow_index + 1) % len(self.choices)
                state.controller.isDownPressed = False

        # Check if the "T" key is pressed and the flag is not set
        if current_message.is_finished() and current_message.message_at_end() and state.controller.isTPressed:

            selected_option = self.choices[self.arrow_index]
            print(f"Selected option: {selected_option}")

            # Check if the selected option is "Yes" and execute the code you provided
            if selected_option == "Yes":
                print("YES")

                # state.currentScreen = state.crapsBossScreen
                # state.crapsBossScreen.start(state)

                state.currentScreen = state.crapsBossScreen
                state.crapsBossScreen.start(state)

            # Reset the flag when the "T" key is released
            if not state.controller.isTPressed:
                self.t_pressed = False

        if state.controller.isTPressed and current_message.is_finished():
            state.controller.isTPressed = False
            # Exiting the conversation
            self.state = "waiting"
            self.menu_index = 0
            self.arrow_index = 0
            self.state_start_time = pygame.time.get_ticks()

            # Unlock the player to allow movement
            state.player.canMove = True

    def draw(self, state):
        # rect = (
        #     self.collision.x + state.camera.x, self.collision.y + state.camera.y,
        #     self.collision.width, self.collision.height)
        # pygame.draw.rect(state.DISPLAY, self.color, rect)

        sprite_rect = pygame.Rect(7, 6, 84, 80)

        # Get the subsurface for the area you want
        sprite = self.character_sprite_image.subsurface(sprite_rect)

        # Scale the subsurface to make it two times bigger
        scaled_sprite = pygame.transform.scale(sprite, (77, 77))  # 44*2 = 88

        # Define the position where you want to draw the sprite
        sprite_x = self.collision.x + state.camera.x - 20
        sprite_y = self.collision.y + state.camera.y - 10

        # Draw the scaled sprite portion on the display
        state.DISPLAY.blit(scaled_sprite, (sprite_x, sprite_y))

        if self.state == "talking":
            current_message = (
                self.black_jack_thomas_messages["welcome_message"]
                if state.player.hasRabies
                else (
                    self.black_jack_thomas_messages["welcome_message"]

                )
            )

            current_message.draw(state)

            # Draw the "Yes/No" box only on the last message
            if current_message.is_finished() and current_message.message_at_end():
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
