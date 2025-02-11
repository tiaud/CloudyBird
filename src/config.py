import pygame
import os

pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cloudy Bird")

BASE_PATH = os.path.dirname(os.path.dirname(__file__))  # Get the main project folder
ASSETS_PATH = os.path.join(BASE_PATH, "assets")

# Load images and optimize for blitting
bg_img = pygame.image.load(os.path.join(ASSETS_PATH, "background.png")).convert()
bird_img = pygame.image.load(os.path.join(ASSETS_PATH, "bird.png")).convert_alpha()
pipe_img = pygame.image.load(os.path.join(ASSETS_PATH, "pipe.png")).convert_alpha()

# Load and configure music
pygame.mixer.music.load(os.path.join(ASSETS_PATH, "main theme.mp3"))

# Configuing the window icon
pygame_icon = pygame.image.load(os.path.join(ASSETS_PATH, "bird.png")).convert_alpha()
pygame.display.set_icon(pygame_icon)

# Load font
font = pygame.font.Font(os.path.join(ASSETS_PATH, "Pokemon GB.ttf"), 16)

# High score file and value
high_score_file = "highscore.txt"
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as f:
        high_score = int(f.read().strip())
else:
    high_score = 0

# Game state flag (controlled via the main loop)
game_start = False