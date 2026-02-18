import pygame
from game_text import GameText


class Score(GameText):
    def __init__(self, color, font_size, font):
        super().__init__(color, font_size, font)
        self.score = 0

    def update_score(self, points):
        self.score += points

    def draw(self, screen):
        self.image = self.font.render(f"Score: {self.score}", True, self.color)
        self.rect = self.image.get_rect(topright=(screen.get_width() - 50, 10))
        screen.blit(self.image, self.rect)
