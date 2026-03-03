import pygame
import constants
from circleshape import CircleShape
from constants import BOMB_RADIUS_GROWTH, BOMB_TTL
from explosion import Explosion


class Bomb(Explosion):
    def __init__(self, x, y, radius=5):
        super().__init__(x, y, radius, lifespan=BOMB_TTL, radius_growth=100)

