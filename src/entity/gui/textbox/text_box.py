import textwrap

import pygame

from entity.entity import Entity


class TextBox(Entity):
    def __init__(self, messages: list[str], rect: tuple[int, int, int, int],
                 font_size: int, delay: int, ):
        super().__init__(rect[0], rect[1], rect[2], rect[3])
        self.messages = messages
        self.message_index = 0
        self.text = self.messages[self.message_index]
        self.characters_to_display = 0
        self.font_size = font_size
        self.delay = delay
        self.time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)

    def update(self, state: "GameState"):
        controller = state.controller

        # show characters of text one at a time, not whole message.
        if self.characters_to_display < len(self.text):
            self.characters_to_display += 1

        # handle button press to see next message
        if controller.isTPressed and \
                pygame.time.get_ticks() - self.time > self.delay and \
                self.message_index < len(self.messages) - 1:
            self.time = pygame.time.get_ticks()
            self.message_index += 1
            self.text = self.messages[self.message_index]
            self.characters_to_display = 0
            state.controller.isTPressed = False

        # print("is finished? " + str(self.is_finished()))

    def draw(self, state: "GameState"):
        text_to_display = self.text[:self.characters_to_display]
        wrapped_text = textwrap.wrap(text_to_display, 58)
        for i, line in enumerate(wrapped_text):
            text_surface = self.font.render(line, True, (255, 255, 255))
            state.DISPLAY.blit(text_surface,
                         (self.position.x, self.position.y + (i * 40)))

    def is_finished(self) -> bool:
        return self.message_index == len(self.messages) - 1 and \
            pygame.time.get_ticks() - self.time > self.delay

    # def is_finished(self) -> bool:
    #     is_last_message = self.message_index == len(self.messages) - 1
    #     is_delay_passed = pygame.time.get_ticks() - self.time > self.delay
    #     is_all_characters_displayed = self.characters_to_display == len(self.text)
    #
    #     return is_last_message and is_delay_passed and is_all_characters_displayed

    def reset(self):
        """Resets the TextBox to its initial state."""
        self.message_index = 0
        self.text = self.messages[self.message_index]
        self.characters_to_display = 0
        self.time = pygame.time.get_ticks()  # Reset the timer as well

