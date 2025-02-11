import pygame
import config

class Bird:
    """Represents the player-controlled bird."""

    def __init__(self):
        self.x = 50
        self.y = config.HEIGHT // 2
        self.velocity = 0
        self.gravity = 1
        self.jump_strength = -8.5
        self.image = config.bird_img
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.hitbox = pygame.Rect(
            self.x, self.y,
            self.image.get_width() - 8,
            self.image.get_height() - 16
        )

    def jump(self):
        """Set the upward velocity for a jump."""
        self.velocity = self.jump_strength

    def move(self):
        """Update the bird's position if the game is active."""
        if config.game_start:
            self.velocity += self.gravity
            self.y += self.velocity
            self.rect.y = self.y
            self.hitbox.y = self.y + 8

            # Prevent the bird from moving off the screen
            if self.y < 0:
                self.y = 0
            if self.y > config.HEIGHT - self.image.get_height():
                self.y = config.HEIGHT - self.image.get_height()

    def draw(self, screen):
        """Draw the bird to the given screen."""
        screen.blit(self.image, (self.x, self.y))