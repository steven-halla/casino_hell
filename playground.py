import pygame


class TextBox:
    def __init__(self, text, font_size, delay):
        self.text = text
        self.font_size = font_size
        self.delay = delay
        self.index = 0

    def display(self, screen, position):
        font = pygame.font.Font(None, self.font_size)
        if self.index < len(self.text):
            sub_text = self.text[:self.index + 1]
            text_surface = font.render(sub_text, True, (255, 255, 255))
            screen.blit(text_surface, position)
            self.index += 1
            pygame.display.update()
            clock.tick(self.delay)
        else:
            text_surface = font.render(self.text, True, (255, 255, 255))
            screen.blit(text_surface, position)
            pygame.display.update()

class Screen(TextBox):
    def __init__(self, font_size, delay):
        self.messages = ["This is message 1", "This is message 2", "This is message 3"]
        self.message_index = 0
        super().__init__(self.messages[self.message_index], font_size, delay)
        self.time = pygame.time.get_ticks()
        self.delay = delay

    def update(self):
        if pygame.time.get_ticks() - self.time > self.delay:
            self.index += 1
            self.time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.index >= len(self.text):
                self.index = 0
                self.message_index += 1
                if self.message_index >= len(self.messages):
                    self.message_index = 0
                self.text = self.messages[self.message_index]
                self.time = pygame.time.get_ticks()
    def draw(self, screen, position):
        font = pygame.font.Font(None, self.font_size)
        if self.index < len(self.text):
            sub_text = self.text[:self.index + 1]
            text_surface = font.render(sub_text, True, (255, 255, 255))
            screen.blit(text_surface, position)
            pygame.display.update()
        else:
            text_surface = font.render(self.text, True, (255, 255, 255))
            screen.blit(text_surface, position)
            pygame.display.update()




# Initialize pygame
pygame.init()

# Set the window size
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Text Box Example")

# Create a text box object
text_box = Screen(30, 7.5)

# Set the initial position of the text
text_rect = pygame.Rect(size[0] // 2, size[1] // 2, 0, 0)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with black
    screen.fill((0, 0, 0))

    for i in range(1):
        text_box.update()
    text_box.draw(screen, text_rect)
    pygame.display.flip()

