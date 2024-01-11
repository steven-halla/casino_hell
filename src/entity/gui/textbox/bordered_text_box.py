from entity.entity import Entity
from entity.gui.textbox.bordered_box import BorderedBox
from entity.gui.textbox.text_box import TextBox


class BorderedTextBox(Entity):
    def __init__(self, messages: list[str], rect: tuple[int, int, int, int],
                 font_size: int, delay: int):
        super().__init__(rect[0], rect[1], rect[2], rect[3])
        self.border_box = BorderedBox(rect)
        padding = self.border_box.border_width + 10
        text_box_rect = (
        rect[0] + padding, rect[1] + padding, rect[2] - padding * 2,
        rect[3] - padding * 2)
        self.text_box = TextBox(messages, text_box_rect, font_size, delay)

    def update(self, state: "GameState"):
        self.border_box.update(state)
        self.text_box.update(state)

    def draw(self, state: "GameState"):
        self.border_box.draw(state)
        self.text_box.draw(state)

    def is_finished(self) -> bool:
        return self.text_box.is_finished()
