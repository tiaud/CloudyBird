import pygame, os, config

class Bird:
    def __init__(self):
        self.x = 50
        self.y = config.HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.9
        self.jump_strength = -9

        self.images = [pygame.image.load(os.path.join(config.ASSETS_PATH, f"bird{num}.png")).convert_alpha() for num in range(1, 4)]
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.hitbox = pygame.Rect(self.rect.x + 4, self.rect.y + 8,
                                  self.image.get_width() - 8, self.image.get_height() - 16)
        self.angle = 0

    def jump(self):
        self.velocity = self.jump_strength

    def move(self):
        if config.game_start:
            self.velocity = min(self.velocity + self.gravity, 8)
            self.y += self.velocity
            self.rect.centery = self.y
            self.hitbox.centery = self.y + 8
            self.angle = self.velocity * -2
            self.counter += 1
            if self.counter > 5:
                self.counter = 0
                self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]
            self.y = max(0, min(self.y, config.HEIGHT - self.image.get_height()))

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated.get_rect(center=self.rect.center)
        screen.blit(rotated, new_rect.topleft)
        
    def reset(self):
        self.velocity = 0
        self.y = config.HEIGHT // 2
        self.rect.centery = self.y
        self.hitbox.centery = self.y + 8
        self.angle = 0
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]