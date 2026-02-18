from game_text import GameText


class PlayerHealthText(GameText):
    def __init__(self, color, font_size, player=None, font=None):
        super().__init__(color, font_size, font)
        self.player = player

    def draw(self, screen):
        self.image = self.font.render(f"Lives: {self.player.lives}", True, "red")
        self.rect = self.image.get_rect(topleft=(30, 10))
        screen.blit(self.image, self.rect)
