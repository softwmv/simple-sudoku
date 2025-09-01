class NumberSelection:
    def __init__(self, pygame, font):
        self.pg = pygame
        self.btn_width, self.btn_height = 80, 80
        self.font = font
        self.selected_num = 0
        
        self.btn_color = (202, 211, 245)
        self.selected_color = (114, 135, 253)
        self.btn_positions = [
            (200, 785), (290, 785), (380, 785),
            (470, 785), (560, 785), (650, 785),
            (740, 785), (830, 785), (920, 785)
        ]

    def draw_buttons(self, surface):
        for index, pos in enumerate(self.btn_positions):
            self.pg.draw.rect(surface, self.btn_color, (pos[0], pos[1], self.btn_width, self.btn_height),
                            width=2, border_radius=5)
            if self.button_hover(pos):
                self.pg.draw.rect(surface, self.selected_color, (pos[0], pos[1], self.btn_width, self.btn_height),
                            width=2, border_radius=5)
                text_surface = self.font.render(str(index + 1), True, self.selected_color)
            else:
                text_surface = self.font.render(str(index + 1), True, self.btn_color)

            # Draw selected button
            if self.selected_num > 0:
                if self.selected_num - 1 == index:
                    self.pg.draw.rect(surface, self.selected_color, (pos[0], pos[1], self.btn_width, self.btn_height),
                            width=2, border_radius=5)
                    text_surface = self.font.render(str(index + 1), True, self.selected_color)
            surface.blit(text_surface, (pos[0] + 35, pos[1] + 30))


    def button_click(self, x: int, y: int) -> None:
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(x, y, pos):
                self.selected_num = index + 1

    def button_hover(self, pos: tuple) -> bool | None:
        mouse_pos = self.pg.mouse.get_pos()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True

    def on_button(self, x: int, y: int, pos: tuple) -> bool:
        return x > pos[0] and x < (pos[0] + self.btn_width) and y > pos[1] and y < (pos[1] + self.btn_height)

