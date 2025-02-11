import random
import pygame
import config

class Pipe:
    """Represents a pair of pipes (obstacles) in the game."""
    def __init__(self, x):
        self.x = x
        self.gap = random.randint(100, 180)
        max_top = 270
        self.top_height = random.randint(170, max_top)
        self.bottom_y = random.randint(330, 430)
        self.rect_top = pygame.Rect(
            self.x - 3, 0,
            config.pipe_img.get_width() - 3,
            self.top_height - 4
        )
        self.rect_bottom = pygame.Rect(
            self.x - 3, self.bottom_y,
            config.pipe_img.get_width() - 3,
            config.HEIGHT - self.bottom_y - 4
        )
        self.passed = False

    def move(self):
        """Move the pipe to the left if the game is active."""
        if config.game_start:
            self.x -= 3
            self.rect_top.x = self.x
            self.rect_bottom.x = self.x

    def draw(self, screen):
        """Draw both the top and bottom pipes."""
        screen.blit(
            pygame.transform.flip(config.pipe_img, False, True),
            (self.x, self.top_height - config.pipe_img.get_height())
        )
        screen.blit(config.pipe_img, (self.x, self.bottom_y))