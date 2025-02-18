import random, pygame, config

class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap = random.randint(120, 200)
        max_top = 270
        self.top_height = random.randint(170, max_top)
        self.bottom_y = self.top_height + self.gap
        self.rect_top = pygame.Rect(self.x - 3, 0, config.pipe_img.get_width() - 3, self.top_height - 4)
        self.rect_bottom = pygame.Rect(self.x - 3, self.bottom_y, config.pipe_img.get_width() - 3, config.HEIGHT - self.bottom_y - 4)
        self.passed = False

    def move(self, speed_factor=1.0):
        if config.game_start:
            self.x -= 4 * speed_factor
            self.rect_top.x = self.x
            self.rect_bottom.x = self.x

    def draw(self, screen):
        screen.blit(pygame.transform.flip(config.pipe_img, False, True),
                    (self.x, self.top_height - config.pipe_img.get_height()))
        screen.blit(config.pipe_img, (self.x, self.bottom_y))