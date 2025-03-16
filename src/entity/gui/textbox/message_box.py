import textwrap
import pygame
from entity.entity import Entity


class MessageBox(Entity):
    DEFAULT_RECT = (65, 460, 700, 130)
    DEFAULT_FONT_SIZE = 36
    DEFAULT_DELAY = 500

    def __init__(self, messages: list[str], rect: tuple[int, int, int, int] = None,
                 font_size: int = None, delay: int = None):
        rect = rect if rect is not None else self.DEFAULT_RECT
        font_size = font_size if font_size is not None else self.DEFAULT_FONT_SIZE
        delay = delay if delay is not None else self.DEFAULT_DELAY

        super().__init__(rect[0], rect[1], rect[2], rect[3])
        self.messages = messages
        self.message_index = 0
        self.characters_to_display = 0
        self.font_size = font_size
        self.delay = delay
        self.time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, font_size)

    def update(self, state: "GameState"):
        controller = state.controller

        # Show characters of text one at a time, not the whole message.
        if self.characters_to_display < len(self.messages[self.message_index]):
            self.characters_to_display += 1

        # Handle button press to see the next message.
        if controller.isTPressed or controller.isAPressedSwitch and \
                pygame.time.get_ticks() - self.time > self.delay and \
                self.message_index < len(self.messages) - 1:
            self.time = pygame.time.get_ticks()
            self.message_index += 1
            self.characters_to_display = 0
            state.controller.isTPressed = False

    def draw(self, state: "GameState"):
        text_to_display = self.messages[self.message_index][:self.characters_to_display]
        wrapped_text = textwrap.wrap(text_to_display, 58)
        for i, line in enumerate(wrapped_text):
            text_surface = self.font.render(line, True, (255, 255, 255))
            state.DISPLAY.blit(text_surface, (self.position.x, self.position.y + (i * 40)))

    def is_finished(self) -> bool:
        return self.message_index == len(self.messages) - 1 and \
            pygame.time.get_ticks() - self.time > self.delay

    def reset(self):
        """Resets the MessageBox to its initial state."""
        self.message_index = 0
        self.characters_to_display = 0
        self.time = pygame.time.get_ticks()  # Reset the timer as well

    def current_message_finished(self):
        """Checks if the current message is displaying its last letter."""
        return self.characters_to_display == len(self.messages[self.message_index])

    def update_message(self, new_message: str):
        """Update the message and reset the display settings."""
        self.messages = [new_message]  # Replace the current message list with the new message
        self.message_index = 0  # Reset message index to the first message
        self.characters_to_display = 0  # Start displaying the message from the first character
        self.time = pygame.time.get_ticks()


