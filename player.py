import sys
import pygame
from bomb import Bomb
from constants import (
    PLAYER_BOMB_COOLDOWN_SECONDS,
    PLAYER_INITIAL_BOMB_COUNT,
    PLAYER_RADIUS,
    LINE_WIDTH,
    PLAYER_SHIELD_ACTIVE_SECONDS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOTING_MAX_TIME,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SCREEN_HEIGHT,
)
from circleshape import CircleShape
from game_text import GameText
from pickup import BombPickup, ShieldPickup, SuperShotPickup, TripleShotPickup
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
        self.shot_type = Shot
        self.shot_timer = PLAYER_SHOOTING_MAX_TIME
        self.bomb_timer = PLAYER_BOMB_COOLDOWN_SECONDS
        self.shield_timer = PLAYER_SHIELD_ACTIVE_SECONDS
        self.num_bombs = PLAYER_INITIAL_BOMB_COUNT
        self.bomb_image = pygame.image.load('bomb_pickup.png').convert_alpha()
        self.bomb_image = pygame.transform.scale(self.bomb_image, (30, 30))
        self.is_shield_active = True
        self.shield_radius = self.radius * 2
        self.shield_text = pygame.font.SysFont("arial", 24)

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
        # self.draw_player_debug_text(screen)
        self.draw_player_movement(screen)
        self.draw_bombs(screen)
        if self.is_shield_active:
            pygame.draw.circle(screen, "blue", self.position, self.shield_radius, LINE_WIDTH)
            text_image = self.shield_text.render(f"Time left for shield: {self.shield_timer:.2f}", True, "Blue")
            rect = text_image.get_rect(topleft=(30, 100))
            screen.blit(text_image, rect)

    def draw_bombs(self, screen):
        for i in range(self.num_bombs):
            rect = self.bomb_image.get_rect(bottomleft=(30 * i, SCREEN_HEIGHT - 10))
            screen.blit(self.bomb_image, rect)

    def draw_player_debug_text(self, screen):
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
        self.shot_timer -= dt
        self.bomb_timer -= dt
        self.shield_timer -= dt

        if self.shield_timer <= 0:
            self.is_shield_active = False

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
        if keys[pygame.K_LCTRL]:
            self.bomb()

    def shoot(self):
        if self.timer > 0:
            return
        self.timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        if self.shot_timer <= 0:
            self.shot_type = Shot
        self.shot_type(self.position.x, self.position.y, self.rotation)
        

    def bomb(self):
        if self.bomb_timer > 0 or self.num_bombs <= 0:
            return

        self.num_bombs -= 1
        self.bomb_timer = PLAYER_BOMB_COOLDOWN_SECONDS
        Bomb(self.position.x, self.position.y)

    def gain_pickup(self, pickup):
        self.shot_timer = PLAYER_SHOOTING_MAX_TIME
        if type(pickup) == TripleShotPickup:
            self.shot_type = TripleShot
        elif type(pickup) == SuperShotPickup:
            self.shot_type = SuperShot
        elif type(pickup) == BombPickup:
            self.num_bombs += 1
        elif type(pickup) == ShieldPickup:
            self.is_shield_active = True
            self.shield_timer = PLAYER_SHIELD_ACTIVE_SECONDS
    
    def collide_with(self, other):
        if self.is_shield_active:
            distance = self.position.distance_to(other.position)
            return self.shield_radius + other.radius >= distance
        return super().collide_with(other)