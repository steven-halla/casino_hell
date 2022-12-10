import pygame

pygame.init()

WINDOWS_SIZE: [int, int] = [500, 500]
display = pygame.display.set_mode(WINDOWS_SIZE)
pygame.display.set_caption("Shooter")
GREEN: (int, int, int) = (0, 255, 0)
BLUE: (int, int, int) = (0, 0, 255)
RED: (int, int, int) = (255, 0, 0)
TILE_SIZE = 32
running = True

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def toTuple(self):
        return (self.x, self.y, self.width, self.height)

    #           ---------- (x2+width,y2+height)
    # (x,y+height)        |
    #   -------------     |
    #  |        |    |    |
    #  |        -----|---- (x2+width2,y2)
    #  |    (x2,y2)  |
    #   -------------
    # (x,y)         (x+width,y)

    #  r: Rectangle =>
    def isOverlap(self, r):
        # print("hi")

        return self.x < r.x + r.width and self.x + self.width > r.x \
               and self.y < r.y + r.height and self.y + self.height > r.y


class Entity:
    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.collision = Rectangle(x, y, width, height)

    def draw(self, display):
        pygame.draw.rect(display, RED, self.collision.toTuple())

    def update(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.collision.x = self.position.x
        self.collision.y = self.position.y
        # print("update entity")
        # print(self.position)
        # print(self.velocity)

    def isOverlap(self, entity):
        return self.collision.isOverlap(entity.collision)

    print("entitiy class shoutout")


class Controller:
    def __init__(self):
        self.isLeftPressed = False
        self.isRightPressed = False
        self.isUpPressed = False
        self.isDownPressed = False
        self.isExitPressed = False

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isExitPressed = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.isLeftPressed = True
                elif event.key == pygame.K_RIGHT:
                    self.isRightPressed = True
                if event.key == pygame.K_UP:
                    self.isUpPressed = True
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.isLeftPressed = False
                elif event.key == pygame.K_RIGHT:
                    self.isRightPressed = False
                if event.key == pygame.K_UP:
                    self.isUpPressed = False
                elif event.key == pygame.K_DOWN:
                    self.isDownPressed = False


class Player(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE)
        self.color = RED
        self.controller = Controller()

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.collision.toTuple())

    def update(self):
        self.controller.update()

        if self.controller.isExitPressed:
            global running
            running = False

        if self.controller.isLeftPressed:
            self.velocity.x = -5
        elif self.controller.isRightPressed:
            self.velocity.x = 5
        else:
            # hard stop
            # self.velocity.x = 0  # default velocity to zero unless key pressed
            # slow stop
            self.velocity.x *= 0.65 # gradually slow the x velocity down
            if abs(self.velocity.x) < 0.15: # if x velocity is close to zero, just set to zero
                self.velocity.x = 0


        if self.controller.isUpPressed:
            self.velocity.y = -5
        elif self.controller.isDownPressed:
            self.velocity.y = 5
        else:
            # hard stop
            # self.velocity.y = 0  # default velocity to zero unless key pressed
            # slow stop
            self.velocity.y *= 0.65 # gradually slow the y velocity down
            if abs(self.velocity.y) < 0.15: # if y velocity is close to zero, just set to zero
                self.velocity.y = 0

        super().update()


class Enemy(Entity):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 100, 100)
        self.color = BLUE

    def draw(self, display):
        pygame.draw.rect(display, self.color, self.collision.toTuple())

    def update(self):
        super().update()


class Game:
    def __init__(self):
        self.player = Player(50, 100)
        self.enemy = Enemy(170, 70)

    def start(self):
        while running:
            # update entities and handle collision
            self.player.update()
            self.enemy.update()

            if self.enemy.isOverlap(self.player):
                print("player overlapped with enemy")

            # render everything
            display.fill((124, 164, 114))

            self.player.draw(display)
            self.enemy.draw(display)

            # update the screen
            pygame.display.update()

        # close Pygame when the game loop is finished
        pygame.quit()


game = Game()
game.start()