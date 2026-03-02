import random
import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from explosion import Explosion
from logger import log_event
from screen_wrapper import ScreenWrapper


class Asteroid(CircleShape, ScreenWrapper):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = self.generate_asteroid_shape()

    def generate_asteroid_shape(self):
        points = []
        num_points = random.randint(8, 12)

        for i in range(num_points):
            angle = (360 / num_points) * i
            variation = random.uniform(0.7, 1.0)
            distance = self.radius * variation
            point = pygame.Vector2(distance, 0).rotate(angle)
            points.append(point)

        return points

    def draw(self, screen):
        size = int(self.radius * 2)
        temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)

        relative_points = [
            (self.radius, self.radius) + offset for offset in self.points
        ]
        pygame.draw.polygon(temp_surface, (255, 255, 255), relative_points, 0)

        texture = pygame.image.load("asteroid_texture.png").convert_alpha()
        texture = pygame.transform.scale(texture, (size, size))

        temp_surface.blit(texture, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(
            temp_surface, (self.position.x - self.radius, self.position.y - self.radius)
        )

    def update(self, dt):
        self.wrap_position()
        self.position += self.velocity * dt

    def add_explosion(self):
        Explosion(self.position.x, self.position.y, self.radius * 0.5)

    def split(self):
        self.kill()
        self.add_explosion()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        new_angle = random.uniform(20, 50)
        vector1 = self.velocity.rotate(new_angle)
        vector2 = self.velocity.rotate(-new_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = vector1 * 1.2
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = vector2 * 1.2
