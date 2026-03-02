import sys
import pygame
from constants import (
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from circleshape import CircleShape
from game_text import GameText
from screen_wrapper import ScreenWrapper
from shot import Shot, SuperShot, TripleShot


class Player(CircleShape, ScreenWrapper):
    def __init__(self, x, y, lives):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.lives = lives
        self.acceleration = 1
        self.max_acceleration = 3
        self.was_accelerating = False
        self.acceleration_text = GameText("red", 20)
        self.image = pygame.image.load("starship.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (self.radius * 2, self.radius * 2)
        )

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def jet_triangle(self, scale_vertical, scale_horizontaly):
        backward = pygame.Vector2(0, 1).rotate(self.rotation + 180)
        right = (
            pygame.Vector2(0, 1).rotate(self.rotation + 90)
            * self.radius
            * scale_horizontaly
        )

        tip = self.position + (backward * self.radius * scale_vertical)
        base_center = self.position + backward * self.radius
        left_point = base_center - right
        right_point = base_center + right
        return [tip, left_point, right_point]

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, -self.rotation + 180)
        rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, rect)
        self.draw_player_text(screen)
        self.draw_player_movement(screen)

    def draw_player_text(self, screen):
        text_image = self.acceleration_text.font.render(
            f"acc: {self.acceleration:.2f}", True, self.acceleration_text.color
        )
        rect = text_image.get_rect(
            topleft=(self.position.x - 100, self.position.y - 20)
        )

        screen.blit(text_image, rect)

    def draw_player_movement(self, screen):
        if not self.was_accelerating:
            return
        jet_triangle_large = self.jet_triangle(
            scale_vertical=2, scale_horizontaly=1 / 2
        )
        pygame.draw.polygon(screen, "orange", jet_triangle_large, 0)

        if self.acceleration > 2.5:
            jet_triangle_small = self.jet_triangle(
                scale_vertical=1.5, scale_horizontaly=1 / 3
            )
            pygame.draw.polygon(screen, "red", jet_triangle_small, 0)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            print("Game Over!")
            sys.exit()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = (
            rotated_vector * PLAYER_SPEED * dt * self.acceleration
        )
        self.position += rotated_with_speed_vector

    def change_acceleration(self, dt):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] and keys[pygame.K_s]) or not keys[pygame.K_w]:
            self.acceleration = 1
        elif keys[pygame.K_w] and self.was_accelerating:
            self.acceleration = min(
                self.max_acceleration, self.acceleration + (2.5 * dt)
            )

        if keys[pygame.K_w]:
            self.was_accelerating = True
        else:
            self.was_accelerating = False

    def update(self, dt):
        self.wrap_position()
        self.timer -= dt
        keys = pygame.key.get_pressed()
        self.change_acceleration(dt)

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        if self.timer > 0:
            return
        self.timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = SuperShot(self.position.x, self.position.y, self.rotation)
