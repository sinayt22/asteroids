import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, PLAYER_SHOOT_SPEED, SHOT_RADIUS, SUPER_SHOT_TTL


class Shot(CircleShape):
    def __init__(self, x, y, rotation, image_path='laser_shot_1.png'):
        super().__init__(x, y, SHOT_RADIUS)
        self.rotation = rotation
        self.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        size = int(self.radius * 2)
        self.texture = pygame.image.load(image_path).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (size * 2, size * 2))
        self.texture = pygame.transform.rotate(self.texture, -self.rotation + 90)
        

    def draw(self, screen):
        temp_surface = self.texture.get_rect(center=self.position)
        screen.blit(self.texture, temp_surface)

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

class SuperShot(Shot):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, rotation, image_path='laser_shot_2.png')
        self.time_to_live = SUPER_SHOT_TTL
    
    def kill(self):
        pass

    def update(self, dt):
        super().update(dt)
        if self.time_to_live - dt <= 0:
            super().kill()

