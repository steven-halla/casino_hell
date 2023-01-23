import pygame

pygame.init()

screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)

sprite_sheet = pygame.image.load("images/playingcards.png")
# first number is width, 2nd is height
sprite_size = (67, 95)
suit_index = {
    "clubs": 0,
    "diamonds": 1,
    "hearts": 2,
    "spades": 3
}

value_index = {
    "2": 0,
    "3": 1,
    "4": 2,
    "5": 3,
    "6": 4,
    "7": 5,
    "8": 6,
    "9": 7,
    "10": 8,
    "jack": 9,
    "queen": 10,
    "king": 11,
    "ace": 12
}

card_width = 68
card_height = 98


def draw_top_card(position: tuple[int, int]):
    top_card_position = (card_width * 13, 0)
    sprite = sprite_sheet.subsurface(pygame.Rect(top_card_position, (card_width, card_height)))
    sprite.set_colorkey((0, 190, 0))
    screen.blit(sprite, position)

def draw_card(suit: str, value: str, position: tuple[int, int]):
    x_offset = value_index[value]
    y_offset = suit_index[suit]
    card_position = (x_offset * card_width, y_offset * card_height)
    sprite = sprite_sheet.subsurface(pygame.Rect(card_position, (card_width, card_height)))
    sprite.set_colorkey((0, 190, 0))
    screen.blit(sprite, position)


cards = [
    ("clubs", "2"),
    ("clubs", "3"),
    ("clubs", "4"),
    ("clubs", "ace"),
    ("diamonds", "king"),
    ("hearts", "10"),
    ("spades", "jack")
]


draw_top_card((0, 0))

i = 0
for card in cards:
    draw_card(card[0], card[1], ((card_width - 30) * i, 100))
    i += 1
# draw_card("spades", "ace", (100, 100))


# sprite_pos_2_clubs = (1, 1)
# sprite_pos2_3_clubs = (70, 1)
# #
# sprite_pos1_3_diamonds = (70, 100)
# sprite_pos3_2_diamonds = (1, 100)
#
# sprite = sprite_sheet.subsurface(pygame.Rect(sprite_pos_2_clubs, sprite_size))
# sprite1 = sprite_sheet.subsurface(pygame.Rect(sprite_pos1_3_diamonds, sprite_size))
# sprite2 = sprite_sheet.subsurface(pygame.Rect(sprite_pos2_3_clubs, sprite_size))
# sprite3 = sprite_sheet.subsurface(pygame.Rect(sprite_pos3_2_diamonds, sprite_size))
#
# sprite.set_colorkey((0, 190, 0))
# sprite1.set_colorkey((0, 190, 0))
# sprite2.set_colorkey((0, 190, 0))
# sprite3.set_colorkey((0, 190, 0))
#
#
# screen.blit(sprite, (100, 100))
# screen.blit(sprite1, (200, 200))
# screen.blit(sprite2, (300, 300))
# screen.blit(sprite3, (400, 400))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()
