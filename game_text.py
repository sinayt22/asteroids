import pygame


class GameText(pygame.sprite.Sprite):
    def __init__(self, color, font_size, font=None):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.color = color
        self.font_size = font_size
        self.font = font
        self.font = pygame.font.SysFont(self.font, self.font_size)

    def draw(self, screen):
        pass
