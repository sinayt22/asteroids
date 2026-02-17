import pygame


class Score(pygame.sprite.Sprite):
    def __init__(self, screen):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.screen = screen
        self.color = "orange"
        self.font_size = 30
        self.score = 0
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.update_image()
        self.rect = self.image.get_rect(topright=(self.screen.get_width() - 50, 10))

    def update_score(self, points):
        self.score += points

    def update_image(self):
        self.image = self.font.render(f"Score: {self.score}", True, self.color)

    def draw(self, screen):
        self.update_image()
        self.screen.blit(self.image, self.rect)
