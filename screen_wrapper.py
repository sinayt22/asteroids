from constants import SCREEN_HEIGHT, SCREEN_WIDTH


class ScreenWrapper:
    def wrap_position(self):
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH - self.position.x
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT - self.position.y
