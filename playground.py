import pygame
import random

# Initialize Pygame
pygame.init()

# Set the size of the window
size = (700, 500)
screen = pygame.display.set_mode(size)

# Set the title of the window
pygame.display.set_caption("Green rectangles")

# Set the color of the rectangles
green = (0, 255, 0)

# Create an empty list to store the rectangles
rects = []

# Create a variable to store the size of the rectangles
rect_size = (16, 16)

# Create a function to check for overlaps
def check_overlap(x, y):
    for rect in rects:
        if rect.collidepoint(x, y):
            return True
    return False

# Create a function to draw the rectangles
def draw_rects():
    for rect in rects:
        pygame.draw.rect(screen, green, rect)

# Create a loop to randomly generate the rectangles' starting positions
while len(rects) < 10:
    x = random.randint(250, 450 - rect_size[0])
    y = random.randint(200, 300 - rect_size[1])
    if not check_overlap(x, y):
        rects.append(pygame.Rect(x, y, rect_size[0], rect_size[1]))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the rectangles on the screen
    draw_rects()

    # Update the display
    pygame.display.flip()

# Exit Pygame
pygame.quit()
