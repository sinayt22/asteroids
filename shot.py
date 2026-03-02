import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, PLAYER_SHOOT_SPEED, SHOT_RADIUS


class Shot(CircleShape):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, SHOT_RADIUS)
        self.rotation = rotation
        self.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.texture = pygame.image.load('laser_shot_1.png').convert_alpha()
        size = int(self.radius * 2)
        self.texture = pygame.transform.scale(self.texture, (size, size))
        self.texture_1 = pygame.transform.rotate(self.texture, -self.rotation + 90)
        self.texture_2 = pygame.transform.rotate(self.texture, -self.rotation + 90 - 45)
        self.texture_3 = pygame.transform.rotate(self.texture, -self.rotation + 90 + 45)

    def draw(self, screen):
        temp_surface = self.texture_1.get_rect(center=self.position)
        screen.blit(self.texture_1, temp_surface)

    def update(self, dt):
        self.position += self.velocity * dt

class TripleShot:
    def __init__(self, x, y, rotation):
        self.shot_1 = Shot(x, y, rotation)
        self.shot_2 = Shot(x, y, rotation + 45)
        self.shot_3 = Shot(x, y, rotation - 45)

    def update(self, dt):
        self.shot_1.update(dt)
        self.shot_2.update(dt)
        self.shot_3.update(dt)

    def draw(self, screen):
        self.shot_1.draw(screen)
        self.shot_2.draw(screen)
        self.shot_3.draw(screen)

    