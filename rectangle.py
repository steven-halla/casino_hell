from typing import Tuple


class Rectangle:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        # self.rect = pygame.Rect(x, y, width, height)

    def toTuple(self) -> Tuple[float, float, float, float]:
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
    def isOverlap(self, r: "Rectangle") -> bool:
        # print("hi")

        return self.x < r.x + r.width and self.x + self.width > r.x \
            and self.y < r.y + r.height and self.y + self.height > r.y
