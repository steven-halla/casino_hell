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

        # handle button press to see next message
        if state.controller.isTPressed and \
                pygame.time.get_ticks() - self.time > self.delay and \
                self.message_index < len(self.messages) - 1:
            self.time = pygame.time.get_ticks()
            self.message_index += 1
            self.characters_to_display = 0

        # print("is finished? " + str(self.is_finished()))

        if self.is_finished():
            self.show_shop_menu = True



    def draw(self, state: "GameState"):
        text = self.messages[self.message_index]
        text_to_display = text[:self.characters_to_display]
        wrapped_text = textwrap.wrap(text_to_display, 60)

        # Fixed dimensions for the text box
        box_width = 700  # Set the width of the text box
        box_height = 120  # Set the height of the text box

        # Position of the text box
        box_x = self.position.x
        box_y = self.position.y

        # Draw the black background rectangle
        pygame.draw.rect(state.DISPLAY, (0, 0, 0), (box_x, box_y, box_width, box_height))

        # Draw the text within the text box
        line_height = 40  # Adjust as needed
        for i, line in enumerate(wrapped_text):
            # Calculate the Y position of each line within the box
            text_line_y = box_y + (i * line_height) + 10  # Adding 10 for padding from the top
            text_surface = state.FONT.render(line, True, (255, 255, 255))
            state.DISPLAY.blit(text_surface, (box_x + 10, text_line_y))  # Adding 10 for padding from the left

        if self.show_shop_menu:
            self.draw_shop_menu(state)

        # Adjust the number '60' in the textwrap.wrap function and the padding values as needed

    def set_shop_items(self, items: list[str]):
        self.shop_items = items

    def draw_shop_menu(self, state: "GameState"):
        # Set the dimensions for the shop menu text box
        box_width = 700
        box_height = 400

        # Position of the shop menu text box - Adjust as needed
        box_x = self.position.x
        box_y = self.position.y - box_height - 20  # 20 pixels above the NPC text box

        # Draw the black background rectangle for the shop menu
        pygame.draw.rect(state.DISPLAY, (0, 0, 0), (box_x, box_y, box_width, box_height))

        # Starting offsets for the items and arrow
        item_y_offset = 50
        item_x_offset = 50
        arrow_offset = -40  # Adjust the position of the arrow to the left of the item

        # Draw the title of the shop menu
        shop_title = "Welcome to the Shop!"
        title_surface = state.FONT.render(shop_title, True, (255, 255, 255))
        state.DISPLAY.blit(title_surface, (box_x + 10, box_y + 10))

        # Create an arrow surface to indicate the selected item
        arrow_surface = state.FONT.render("->", True, (255, 255, 255))

        # Draw arrow for the selected item
        arrow_y_position = box_y + item_y_offset + self.selected_item_index * 40
        state.DISPLAY.blit(arrow_surface, (box_x + item_x_offset + arrow_offset, arrow_y_position))

        # Draw each item in the shop_items list
        for item in self.shop_items:
            item_surface = state.FONT.render(item, True, (255, 255, 255))
            state.DISPLAY.blit(item_surface, (box_x + item_x_offset, box_y + item_y_offset))
            item_y_offset += 40  # Increment y-offset for the next item

    def is_finished(self) -> bool:
        return self.message_index == len(self.messages) - 1 and \
            pygame.time.get_ticks() - self.time > self.delay

    def reset(self):
        self.message_index = 0
        self.characters_to_display = 0
        self.time = pygame.time.get_ticks()
