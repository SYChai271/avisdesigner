from .settings import *


class Button:
    def __init__(self, x, y, width, height, colour, text=None, text_colour=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text
        self.text_colour = text_colour

    def draw(self, win):
        if self.text:
            pygame.draw.rect(win, WHITE,
                             (self.x, self.y, self.width, self.height))
            button_font = get_font(18)
            text = button_font.render(self.text, 1, self.text_colour)
            win.blit(text, (self.x + self.width/2 - text.get_width() /
                     2, self.y + self.height/2 - text.get_height()/2))
        else:
            pygame.draw.rect(win, self.colour,
                             (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, self.text_colour,
                         (self.x, self.y, self.width, self.height), 2)

    def clicked(self, pos):
        x, y = pos

        if not (x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height):
            return False
        return True
