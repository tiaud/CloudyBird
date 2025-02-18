import pygame
import config

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation_speed=0.5):
        super().__init__()
        # Keep a reference to the original image for efficient re-rotation.
        self.original_image = config.clouds_img
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.angle = 0
        self.rotation_speed = rotation_speed

    def update(self):
        # Increase the rotation angle and wrap around at 360
        self.angle = (self.angle + self.rotation_speed) % 360
        # Rotate the original image (rotozoom can be a bit more efficient than rotate)
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        # Adjust rect so that the center stays constant
        self.rect = self.image.get_rect(center=self.rect.center)
