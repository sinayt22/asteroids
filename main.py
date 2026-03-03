import sys
import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bomb import Bomb
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from explosion import Explosion
from logger import log_state, log_event
from player import Player
from player_health_text import PlayerHealthText
from score import Score
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background_image = pygame.image.load("stars.png").convert()
    background_image = pygame.transform.scale(
        background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    Asteroid.containers = (asteroids, drawable, updatable)
    AsteroidField.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)
    Player.containers = (updatable, drawable)
    Score.containers = drawable
    PlayerHealthText.containers = drawable
    Explosion.containers = (updatable, drawable)

    asteroid_field = AsteroidField(asteroids, 30)
    score = Score("orange", 36, "Arial")
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 3)
    player_health = PlayerHealthText("red", 36, player, "Arial")

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # screen.fill("black")
        screen.blit(background_image, (0, 0))

        for u in updatable:
            u.update(dt)

        for asteroid in asteroids:
            if asteroid.collide_with(player):
                log_event("player_hit")
                player.lose_life()
                asteroid.split()

            for shot in shots:
                if asteroid.collide_with(shot):
                    log_event("asteroid_shot")
                    score.update_score(10)
                    asteroid.split()
                    shot.kill()
            
            for bomb in bombs:
                if asteroid.collide_with(bomb):
                    log_event("asteroid_bombed")
                    score.update_score(10)
                    asteroid.split()

        for d in drawable:
            d.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
