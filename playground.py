import pygame

pygame.init()

screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)

sprite_sheet = pygame.image.load("images/playingcards.png")
#first number is width, 2nd is height
sprite_size = (67, 95)
sprite_pos = (1, 1)
sprite_pos1 = (70, 100)



sprite = sprite_sheet.subsurface(pygame.Rect(sprite_pos, sprite_size))
sprite1 = sprite_sheet.subsurface(pygame.Rect(sprite_pos1, sprite_size))
sprite.set_colorkey((0, 190, 0))
sprite1.set_colorkey((0, 190, 0))


screen.blit(sprite, (100, 100))
screen.blit(sprite1, (200, 200))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()
