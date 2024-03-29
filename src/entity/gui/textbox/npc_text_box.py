import textwrap

import pygame

from entity.entity import Entity


class NpcTextBox(Entity):
    def __init__(self, messages: list[str], rect: tuple[int, int, int, int],
                 font_size: int, delay: int):
        super().__init__(rect[0], rect[1], rect[2], rect[3])
        self.messages = messages
        self.message_index = 0
        self.characters_to_display = 0
        self.font_size = font_size
        self.delay = delay
        self.time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)
        self.show_shop_menu = False  # New flag for showing shop menu
        self.shop_items = []  # New: List to store shop items
        self.selected_item_index = 0  # New attribute to track selected item index
        self.last_key_time = 0  # Track the time of the last key press for scrolling



    # def populate_with_dummy_data(self):
    #     # Dummy data: a simple array of items
    #     dummy_items = ["Dummy Item 1", "Dummy Item 2", "Dummy Item 3"]
    #     self.set_shop_items(dummy_items)
    #     self.show_shop_menu = True


    def update(self, state: "GameState"):
        # print("textbox update")
        current_time = pygame.time.get_ticks()
        key_scroll_delay = 200  # Time in milliseconds before recognizing another key press

        if state.controller.isUpPressed and (current_time - self.last_key_time > key_scroll_delay):
            self.selected_item_index = max(0, self.selected_item_index - 1)
            self.last_key_time = current_time  # Update the time of the last key press

        elif state.controller.isDownPressed and (current_time - self.last_key_time > key_scroll_delay):
            self.selected_item_index = min(len(self.shop_items) - 1, self.selected_item_index + 1)
            self.last_key_time = current_time  # Update the time of the last key press

        # show characters of text one at a time, not whole message.
        text = self.messages[self.message_index]
        if self.characters_to_display < len(text):
            self.characters_to_display += 1

        if state.controller.isTPressed and current_time - self.time > self.delay:
            # Check if the entire message isn't shown yet
            if self.characters_to_display < len(text):
                # If not, show the full message immediately
                self.characters_to_display = len(text)
                self.time = pygame.time.get_ticks()  # Reset the time to prevent immediate skipping
            else:
                # If the full message is already displayed, and "T" is pressed again,
                # check if there's a next message to move to
                if self.message_index < len(self.messages) - 1:
                    # Move to the next message and start from the beginning of it
                    self.message_index += 1
                    self.characters_to_display = 0  # Reset character count for new message
                    self.time = pygame.time.get_ticks()

                # # handle button press to see next message
        # if state.controller.isTPressed and \
        #         pygame.time.get_ticks() - self.time > self.delay and \
        #         self.message_index < len(self.messages) - 1:
        #     print("Tttttt")
        #     self.time = pygame.time.get_ticks()
        #     self.message_index += 1
        #     self.characters_to_display = 0

        # print("is finished? " + str(self.is_finished()))

        if self.is_finished():
            self.show_shop_menu = True

    import pygame
    import textwrap

    def draw(self, state: "GameState"):
        text = self.messages[self.message_index]
        text_to_display = text[:self.characters_to_display]
        # Wrap text to a maximum of 55 characters per line
        wrapped_text = textwrap.wrap(text_to_display, 55)

        # Fixed dimensions for the text box
        box_width = 700  # Width of the text box
        box_height = 120  # Height of the text box

        # Position of the text box
        box_x, box_y = self.position.x, self.position.y

        # Border dimensions and color
        border_size = 5  # Size of the border around the text box
        border_color = (255, 255, 255)  # White

        # Draw the border rectangle
        pygame.draw.rect(state.DISPLAY, border_color, (box_x - border_size, box_y - border_size, box_width + 2 * border_size, box_height + 2 * border_size))

        # Draw the black background rectangle for the text box
        pygame.draw.rect(state.DISPLAY, (0, 0, 0), (box_x, box_y, box_width, box_height))

        # Draw the text within the text box
        line_height = 40  # Adjust line height as needed
        padding = 10  # Padding for top, left, and right
        for i, line in enumerate(wrapped_text):
            text_line_y = box_y + (i * line_height) + padding  # Apply top padding
            text_surface = state.FONT.render(line, True, (255, 255, 255))
            # Render text with left padding
            state.DISPLAY.blit(text_surface, (box_x + padding, text_line_y))

        # Adjust the number '60' in the textwrap.wrap function and the padding values as needed

    def message_at_end(self) -> bool:
        """Checks if the current message has finished displaying its last letter."""
        current_message = self.messages[self.message_index]
        return self.characters_to_display == len(current_message)
    def is_finished(self) -> bool:
        self.delay = 700
        return self.message_index == len(self.messages) - 1 and \
            pygame.time.get_ticks() - self.time > self.delay

    def reset(self):
        self.message_index = 0
        self.characters_to_display = 0
        self.time = pygame.time.get_ticks()
