import pygame, os

pygame.init()
pygame.mixer.init()


WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cloudy Bird")
FULLSCREEN = False

def toggle_fullscreen():
    global screen, FULLSCREEN, WIDTH, HEIGHT
    FULLSCREEN = not FULLSCREEN
    if FULLSCREEN:
        info = pygame.display.Info()
        native_w, native_h = info.current_w, info.current_h
        target_aspect = 16 / 10
        new_w = native_w
        new_h = int(native_w / target_aspect)
        if new_h > native_h:
            new_h = native_h
            new_w = int(native_h * target_aspect)
        screen = pygame.display.set_mode((native_w, native_h), pygame.FULLSCREEN)
    else:
        WIDTH, HEIGHT = 400, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))


BASE_PATH = os.path.dirname(os.path.dirname(__file__))
ASSETS_PATH = os.path.join(BASE_PATH, "assets")


bg_img = pygame.image.load(os.path.join(ASSETS_PATH, "background.png")).convert_alpha()
bg_img = pygame.transform.scale(bg_img, (HEIGHT * 1.5, HEIGHT))
bird_img = pygame.image.load(os.path.join(ASSETS_PATH, "bird.png")).convert_alpha()
pipe_img = pygame.image.load(os.path.join(ASSETS_PATH, "pipe.png")).convert_alpha()
clouds_img = pygame.image.load(os.path.join(ASSETS_PATH, "clouds.png")).convert_alpha()
clouds_img = pygame.transform.scale(clouds_img, (HEIGHT + (HEIGHT // 3), HEIGHT))

slider_bar_img = pygame.image.load(os.path.join(ASSETS_PATH, "slider_bar.png")).convert_alpha()
slider_knob_img = pygame.image.load(os.path.join(ASSETS_PATH, "slider_knob.png")).convert_alpha()
slider_knob_img = pygame.transform.scale(slider_knob_img, (20, 20))

settings_img = pygame.image.load(os.path.join(ASSETS_PATH, "settings.png")).convert_alpha()
settings_img = pygame.transform.scale(settings_img, (36, 36))


cloud_speed = -0.5
s_interval1, s_interval2 = 1000, 1500

pygame.mixer.music.load(os.path.join(ASSETS_PATH, "main theme.mp3"))
pygame_icon = pygame.image.load(os.path.join(ASSETS_PATH, "bird.png")).convert_alpha()
pygame.display.set_icon(pygame_icon)

font = pygame.font.Font(os.path.join(ASSETS_PATH, "Pokemon GB.ttf"), 16)

high_score_file = "highscore.txt"
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as f:
        high_score = int(f.read().strip())
else:
    high_score = 0


game_start = False
music_on = True
music_volume = 0.3
pygame.mixer.music.set_volume(music_volume)