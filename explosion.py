import pygame

from circleshape import CircleShape


class Explosion(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color = (255, 255, 0)
        self.alpha = 255
        self.max_lifespan = 1
        self.current_lifespan = self.max_lifespan

    def draw(self, screen):
        size = int(self.radius * 2)
        temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)

        pygame.draw.circle(
            temp_surface,
            (*self.color, self.alpha),
            (self.radius, self.radius),
            int(self.radius),
        )
        screen.blit(
            temp_surface, (self.position.x - self.radius, self.position.y - self.radius)
        )

    def update(self, dt):
        self.current_lifespan -= dt
        if self.current_lifespan <= 0:
            self.kill()
            return

        self.radius += 5 * dt

        progress = 1 - (self.current_lifespan / self.max_lifespan)
        if progress < 0.3:
            t = progress / 0.3
            self.color = (255, 255 - int(100 * t), 0)
        elif progress < 0.7:
            t = (progress - 0.3) / 0.4
            self.color = (255, 255 - int(100 * t), 0)
        else:
            self.color = (255, 0, 0)

        self.alpha = int(255 * (1 - progress))
