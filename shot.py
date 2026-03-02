import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, PLAYER_SHOOT_SPEED, SHOT_RADIUS


class Shot(CircleShape):
    def __init__(self, x, y, rotation):
        super().__init__(x, y, SHOT_RADIUS)
        self.rotation = rotation
        self.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def draw(self, screen):
        size = int(self.radius * 2)
        # temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        # pygame.draw.circle(temp_surface, (255, 255, 255), self.position, self.radius, 0)
        
        texture = pygame.image.load('laser_shot_1.png')
        texture = pygame.transform.scale(texture, (size, size))
        texture = pygame.transform.rotate(texture, -self.rotation + 90)
        temp_surface = texture.get_rect(center=self.position)
        
        # temp_surface.blit(texture, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        # screen.blit(temp_surface, (self.position.x - self.radius, self.position.y - self.radius))
        screen.blit(texture, temp_surface)

    def update(self, dt):
        self.position += self.velocity * dt
