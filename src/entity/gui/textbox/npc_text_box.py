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

    def update(self, state: "GameState"):
        # print("textbox update")
        controller = state.controller

        # show characters of text one at a time, not whole message.
        text = self.messages[self.message_index]
        if self.characters_to_display < len(text):
            self.characters_to_display += 1

        # handle button press to see next message
        if controller.isTPressed and \
                pygame.time.get_ticks() - self.time > self.delay and \
                self.message_index < len(self.messages) - 1:
            self.time = pygame.time.get_ticks()
            self.message_index += 1
            self.characters_to_display = 0

        # print("is finished? " + str(self.is_finished()))

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

        # Adjust the number '60' in the textwrap.wrap function and the padding values as needed

    def is_finished(self) -> bool:
        return self.message_index == len(self.messages) - 1 and \
            pygame.time.get_ticks() - self.time > self.delay

    def reset(self):
        self.message_index = 0
        self.characters_to_display = 0
        self.time = pygame.time.get_ticks()
