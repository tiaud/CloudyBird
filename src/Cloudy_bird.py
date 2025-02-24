import pygame, random, os, config
from bird import Bird
from pipe import Pipe

global_cloud_x = 0

def draw_clouds(dt):
    global global_cloud_x 
    global_cloud_x -= config.cloud_speed * dt * 60
    if global_cloud_x >= config.clouds_img.get_width():
        global_cloud_x = 0
    config.screen.blit(config.clouds_img, (global_cloud_x, 0))
    config.screen.blit(config.clouds_img, (global_cloud_x - config.clouds_img.get_width(), 0))

def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.hitbox.colliderect(pipe.rect_top) or bird.hitbox.colliderect(pipe.rect_bottom):
            return True
    return bird.y >= config.HEIGHT - bird.image.get_height()

def draw_score(score):
    score_text = config.font.render(f"Score: {score}", True, (227, 138, 193))
    high_score_text = config.font.render(f"High Score: {config.high_score}", True, (227, 138, 193))
    config.screen.blit(score_text, (10, 10))
    config.screen.blit(high_score_text, (10, 10 + high_score_text.get_height()))

def draw_text_centered(text, y):
    rendered = config.font.render(text, True, (227, 138, 193))
    center_x = config.screen.get_width() // 2
    config.screen.blit(rendered, (center_x - rendered.get_width() // 2, int(y)))

def draw_settings_button():
    pos = (config.screen.get_width() - 50, 10)
    button_rect = pygame.Rect(pos[0], pos[1], config.settings_img.get_width(), config.settings_img.get_height())
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hovered = button_rect.collidepoint(mouse_x, mouse_y)
    scale = 1.2 if hovered else 1.0
    scaled_img = pygame.transform.scale(config.settings_img, (int(config.settings_img.get_width() * scale),
                                                               int(config.settings_img.get_height() * scale)))
    new_rect = scaled_img.get_rect(center=button_rect.center)
    config.screen.blit(scaled_img, new_rect.topleft)

    font_path = os.path.join(config.ASSETS_PATH, "Pokemon GB.ttf")
    small_font = pygame.font.Font(font_path, 8)
    settings_text = small_font.render("Settings", True, (227, 138, 193))
    text_rect = settings_text.get_rect(center=(pos[0] + config.settings_img.get_width() // 2,
                                               pos[1] + config.settings_img.get_height() + 10))
    config.screen.blit(settings_text, text_rect.topleft)
    return button_rect, hovered

def settings_screen():
    clock = pygame.time.Clock()
    slider_width = 150
    slider_height = config.slider_bar_img.get_height()
    slider_x = config.screen.get_width() // 2 - slider_width // 2
    slider_y = 340
    dragging = False

    while True:
        dt = clock.tick(30) / 1000
        config.screen.blit(config.bg_img, (0, 0))
        draw_clouds(dt)
        draw_text_centered("Settings", 150)
        draw_text_centered("Music: ON" if config.music_on else "Music: OFF", 220)
        draw_text_centered("M - mute", 270)
        draw_text_centered("Volume", 310)

        config.screen.blit(config.slider_bar_img, (slider_x, slider_y))
        knob_x = slider_x + int(config.music_volume * slider_width) - config.slider_knob_img.get_width() // 2
        knob_y = slider_y + slider_height // 2 - config.slider_knob_img.get_height() // 2
        config.screen.blit(config.slider_knob_img, (knob_x, knob_y))
        draw_text_centered("Q - quit", 370)
        draw_text_centered("ESC - return", 420)
        draw_text_centered("F - full-screen", 470)
        draw_settings_button()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if config.music_on:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    config.music_on = not config.music_on
                if event.key == pygame.K_q:
                    confirm_quit()
                # ESC or S return from settings
                if event.key in (pygame.K_ESCAPE, pygame.K_s):
                    return
                if event.key == pygame.K_f:
                    config.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
                    if slider_rect.collidepoint(mx, my):
                        dragging = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            if event.type == pygame.MOUSEMOTION and dragging:
                mx, _ = event.pos
                rel_x = max(slider_x, min(mx, slider_x + slider_width)) - slider_x
                config.music_volume = rel_x / slider_width
                pygame.mixer.music.set_volume(config.music_volume)

def start_screen():
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(30) / 1000
        config.screen.blit(config.bg_img, (0, 0))
        draw_clouds(dt)
        draw_text_centered("Cloudy Bird", 200)
        draw_text_centered(f"High Score: {config.high_score}", 250)
        draw_text_centered("Press SPACE to start", 300)
        draw_text_centered("Press ESC to exit", 350)
        draw_text_centered("Press S for settings", 400)
        draw_settings_button()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    confirm_quit()
                if event.key == pygame.K_s:
                    settings_screen()
                if event.key == pygame.K_f:
                    config.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    btn_rect, hovered = draw_settings_button()
                    if hovered:
                        settings_screen()

def confirm_quit():
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(30) / 1000
        config.screen.blit(config.bg_img, (0, 0))
        draw_clouds(dt)
        draw_text_centered("Quit game?", 250)
        draw_text_centered("Y - Yes", 300)
        draw_text_centered("N - No", 350)
        draw_settings_button()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    pygame.quit(); exit()
                if event.key == pygame.K_n:
                    return
                if event.key == pygame.K_f:
                    config.toggle_fullscreen()

def end_screen(score):
    if score > config.high_score:
        config.high_score = score
        with open(config.high_score_file, "w") as f:
            f.write(str(config.high_score))
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(30) / 1000
        config.screen.blit(config.bg_img, (0, 0))
        draw_clouds(dt)
        draw_text_centered(f"Score: {score}", 175)
        draw_text_centered(f"High Score: {config.high_score}", 225)
        draw_text_centered("R - Restart", 275)
        draw_text_centered("M - Main menu", 325)

        draw_text_centered("ESC - Quit", 375)
        draw_text_centered("Press S for settings", 425)
        draw_settings_button()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_m:
                    return "menu"
                if event.key == pygame.K_ESCAPE:
                    confirm_quit()
                if event.key == pygame.K_s:
                    settings_screen()
                if event.key == pygame.K_f:
                    config.toggle_fullscreen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    btn_rect, hovered = draw_settings_button()
                    if hovered:
                        settings_screen()

def game_loop():
    bird = Bird()
    pipes = []
    score = 0
    config.game_start = False
    clock = pygame.time.Clock()
    
    spawn_distance_threshold = 250
    distance_accum = 0
    base_pipe_speed = 4
    speed_factor = 1.0
    
    while True:
        dt = clock.tick(30) / 1000
        config.screen.blit(config.bg_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    config.game_start = True
                    bird.jump()
                elif event.key == pygame.K_f:
                    config.toggle_fullscreen()
                elif event.key == pygame.K_s:
                    settings_screen()
                elif event.key == pygame.K_ESCAPE:
                    settings_screen()
                    config.game_start = False
                    bird.reset()
                    continue

        if config.game_start:
            bird.move()
        bird.draw(config.screen)

        if config.game_start:
            distance_accum += base_pipe_speed * speed_factor * dt * 30
            if distance_accum >= spawn_distance_threshold:
                distance_accum = 0
                new_pipe = Pipe(config.screen.get_width() + spawn_distance_threshold)
                pipes.append(new_pipe)
        
        speed_factor = 1.0 + (score // 5) * 0.1
        for pipe in pipes[:]:
            if config.game_start:
                pipe.move(speed_factor)
            pipe.draw(config.screen)
            if not pipe.passed and pipe.x + config.pipe_img.get_width() < bird.x:
                pipe.passed = True
                score += 1
            if pipe.x < -config.pipe_img.get_width():
                pipes.remove(pipe)

        if check_collision(bird, pipes):
            config.game_start = False
            return "game_over", score

        draw_clouds(dt)
        draw_score(score)
        draw_settings_button()
        pygame.display.update()

def main():
    pygame.mixer.music.set_volume(config.music_volume)
    pygame.mixer.music.play(-1)
    
    while True:
        start_screen()
        
        while True:
            state, score = game_loop()
            if state == "quit":
                pygame.quit()
                exit()
            
            while True:
                action = end_screen(score)
                if action in ("restart", "menu", "quit"):
                    break
            if action == "restart":
                continue
            elif action == "menu":
                break
        
if __name__ == "__main__":
    main()