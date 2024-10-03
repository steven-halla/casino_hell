import textwrap
import pygame
from entity.entity import Entity

class ShopNpcTextBox(Entity):
    def __init__(self, messages: list[str], rect: tuple[int, int, int, int], font_size: int, delay: int):
        super().__init__(rect[0], rect[1], rect[2], rect[3])
        self.messages: list[str] = messages
        self.message_index: int = 0
        self.characters_to_display: int = 0
        self.font_size: int = font_size
        self.delay: int = delay
        self.time: int = pygame.time.get_ticks()
        self.font: pygame.font.Font = pygame.font.Font(None, 36)
        self.show_shop_menu: bool = False
        self.shop_items: list[str] = []
        self.shop_inventory_costs: list[str] = []
        self.selected_item_index: int = 0
        self.last_key_time: int = 0

    def update(self, state: "GameState"):
        current_time: int = pygame.time.get_ticks()
        key_scroll_delay: int = 400

        if self.is_finished():
            if state.controller.isUpPressed and (current_time - self.last_key_time > key_scroll_delay) and state.area2RestScreen.shop_lock == False:
                self.selected_item_index = max(0, self.selected_item_index - 1)
                self.last_key_time = current_time

            elif state.controller.isDownPressed and (current_time - self.last_key_time > key_scroll_delay) and state.area2RestScreen.shop_lock == False:
                self.selected_item_index = min(len(self.shop_items) - 1, self.selected_item_index + 1)
                self.last_key_time = current_time

        text: str = self.messages[self.message_index]
        if self.characters_to_display < len(text):
            self.characters_to_display += 1

        if state.controller.isTPressed and pygame.time.get_ticks() - self.time > self.delay and self.message_index < len(self.messages) - 1:
            self.time = pygame.time.get_ticks()
            self.message_index += 1
            self.characters_to_display = 0

        if self.is_finished():
            self.show_shop_menu = True

    def draw(self, state: "GameState"):
        text: str = self.messages[self.message_index]
        text_to_display: str = text[:self.characters_to_display]
        wrapped_text: list[str] = textwrap.wrap(text_to_display, 60)

        box_width: int = 700
        box_height: int = 120
        box_x: int = self.position.x
        box_y: int = self.position.y

        # Draw the main black rectangle
        pygame.draw.rect(state.DISPLAY, (0, 0, 0), (box_x, box_y, box_width, box_height))

        # Draw the white border around the main rectangle
        border_thickness: int = 3
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), (box_x, box_y, box_width, box_height), border_thickness)

        line_height: int = 40
        for i, line in enumerate(wrapped_text):
            text_line_y: int = box_y + (i * line_height) + 10
            text_surface: pygame.Surface = state.FONT.render(line, True, (255, 255, 255))
            state.DISPLAY.blit(text_surface, (box_x + 10, text_line_y))

        if self.show_shop_menu:
            self.draw_shop_menu(state)

    def set_shop_items(self, items: list[str], inventory_costs: list[str]):
        self.shop_items = items
        self.shop_inventory_costs = inventory_costs

    def draw_shop_menu(self, state: "GameState"):
        box_width: int = 700
        box_height: int = 400
        box_x: float = self.position.x
        box_y: float = self.position.y - box_height - 20

        # Draw the main black rectangle
        pygame.draw.rect(state.DISPLAY, (0, 0, 0), (box_x, box_y, box_width, box_height))

        # Draw the white border around the main rectangle
        border_thickness: int = 3
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), (box_x, box_y, box_width, box_height), border_thickness)

        item_y_offset: int = 50
        item_x_offset: int = 50
        arrow_offset: int = -40

        shop_title: str = "Must have 700 gold after purchase!"
        title_surface: pygame.Surface = state.FONT.render(shop_title, True, (255, 255, 255))
        state.DISPLAY.blit(title_surface, (box_x + 10, box_y + 10))

        arrow_surface: pygame.Surface = state.FONT.render("->", True, (255, 255, 255))
        arrow_y_position: float = box_y + item_y_offset + self.selected_item_index * 40
        state.DISPLAY.blit(arrow_surface, (box_x + item_x_offset + arrow_offset, arrow_y_position))

        for i, item in enumerate(self.shop_items):
            item_surface: pygame.Surface = state.FONT.render(item, True, (255, 255, 255))
            price_surface: pygame.Surface = state.FONT.render(self.shop_inventory_costs[i], True, (255, 255, 255))
            state.DISPLAY.blit(item_surface, (box_x + item_x_offset, box_y + item_y_offset))
            state.DISPLAY.blit(price_surface, (box_x + item_x_offset + 300, box_y + item_y_offset))
            item_y_offset += 40



        # Now draw the smaller box overlapping the top-right corner of the main box
        bot_box_width: int = 175
        bot_box_height: int = 60
        bot_box_x: float = box_x + box_width - bot_box_width + 30
        bot_box_y: float = box_y - 20 # Positioned to overlap the top-right corner

        # Draw the black rectangle for the bot box
        pygame.draw.rect(state.DISPLAY, (0, 0, 0), (bot_box_x, bot_box_y, bot_box_width, bot_box_height))

        # Draw the white border around the bot box
        pygame.draw.rect(state.DISPLAY, (255, 255, 255), (bot_box_x, bot_box_y, bot_box_width, bot_box_height), border_thickness)

        # Optional: Render text or graphics inside the bot box
        bot_text: str = f"Money: {state.player.money}"
        bot_text_surface: pygame.Surface = state.FONT.render(bot_text, True, (255, 255, 255))
        state.DISPLAY.blit(bot_text_surface, (bot_box_x + 10, bot_box_y + 17))

    def is_finished(self) -> bool:
        return self.message_index == len(self.messages) - 1 and pygame.time.get_ticks() - self.time > self.delay

    def reset(self):
        self.message_index = 0
        self.selected_item_index = 0
        self.characters_to_display = 0
        self.time = pygame.time.get_ticks()
