import pygame

from circleshape import CircleShape
import random

from constants import LINE_WIDTH, PICKUP_TIME_SHOWING

class Pickup(CircleShape):
    def __init__(self, x, y, radius, image_path):
        super().__init__(x, y, radius)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (radius, radius))
        self.timer = PICKUP_TIME_SHOWING

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()
        self.position.x += random.randint(-1, 1) * dt * 10
        self.position.y += random.randint(-1, 1) * dt * 10
    
    def draw(self, screen):
        rect = self.image.get_rect(center=(self.position.x, self.position.y))
        pygame.draw.circle(screen, "yellow", self.position, self.radius, LINE_WIDTH)
        screen.blit(self.image, rect)

class TripleShotPickup(Pickup):
    def __init__(self, x, y, radius=30):
        super().__init__(x, y, radius, 'triple_shot_pickup.png')

class SuperShotPickup(Pickup):
    def __init__(self, x, y, radius=30):
        super().__init__(x, y, radius, 'super_shot_pickup.png')

class BombPickup(Pickup):
    def __init__(self, x, y, radius=30):
        super().__init__(x, y, radius, 'bomb_pickup.png')

class ShieldPickup(Pickup):
    def __init__(self, x, y, radius=30):
        super().__init__(x, y, radius, 'shield_pickup.png')