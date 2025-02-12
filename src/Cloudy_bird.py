import pygame
import config
from bird import Bird
from pipe import Pipe


def check_collision(bird, pipes): # Return True if the bird collides with any pipe or the ground.
    for pipe in pipes:
        if bird.hitbox.colliderect(pipe.rect_top) or bird.hitbox.colliderect(pipe.rect_bottom):
            return True
    return bird.y >= config.HEIGHT - bird.image.get_height()


def draw_score(screen, score, high_score): # Draw the score and high score on the screen.
    score_text = config.font.render(f"Score: {score}", True, (227, 138, 193))
    high_score_text = config.font.render(f"High Score: {high_score}", True, (227, 138, 193))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))


def start_screen(): # Display the start screen and wait for the user to press SPACE.
    while True:
        config.screen.blit(config.bg_img, (0, 0))
        title = config.font.render("Cloudy Bird", True, (227, 138, 193))
        high_score_text = config.font.render(f"High Score: {config.high_score}", True, (227, 138, 193))
        start_text = config.font.render("Press SPACE to start", True, (227, 138, 193))
        exit_text = config.font.render("ESC to exit", True, (227, 138, 193))

        config.screen.blit(title, (config.WIDTH // 2 - title.get_width() // 2, 200))
        config.screen.blit(high_score_text, (config.WIDTH // 2 - high_score_text.get_width() // 2, 250))
        config.screen.blit(start_text, (config.WIDTH // 2 - start_text.get_width() // 2, 300))
        config.screen.blit(exit_text, (config.WIDTH // 2 - exit_text.get_width() // 2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    confirm_quit()


def confirm_quit(): # Display a quit confirmation popup
    while True:
        config.screen.blit(config.bg_img, (0, 0))
        message = config.font.render("Quit game?", True, (227, 138, 193))
        yes_text = config.font.render("Y - Yes", True, (227, 138, 193))
        no_text = config.font.render("N - No", True, (227, 138, 193))

        config.screen.blit(message, (config.WIDTH // 2 - message.get_width() // 2, 250))
        config.screen.blit(yes_text, (config.WIDTH // 2 - yes_text.get_width() // 2, 300))
        config.screen.blit(no_text, (config.WIDTH // 2 - no_text.get_width() // 2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_n:
                    return  # Return to the game


def end_screen(score): # Display the end screen, update high score if needed, and return the next action.
    if score > config.high_score:
        config.high_score = score
        with open(config.high_score_file, "w") as f:
            f.write(str(config.high_score))

    while True:
        config.screen.blit(config.bg_img, (0, 0))
        score_text = config.font.render(f"Score: {score}", True, (227, 138, 193))
        high_score_text = config.font.render(f"High Score: {config.high_score}", True, (227, 138, 193))
        restart_text = config.font.render("R - Restart", True, (227, 138, 193))
        menu_text = config.font.render("M - Main menu", True, (227, 138, 193))
        quit_text = config.font.render("ESC - Quit", True, (227, 138, 193))

        config.screen.blit(score_text, (config.WIDTH // 2 - score_text.get_width() // 2, 175))
        config.screen.blit(high_score_text, (config.WIDTH // 2 - high_score_text.get_width() // 2, 225))
        config.screen.blit(restart_text, (config.WIDTH // 2 - restart_text.get_width() // 2, 275))
        config.screen.blit(menu_text, (config.WIDTH // 2 - menu_text.get_width() // 2, 325))
        config.screen.blit(quit_text, (config.WIDTH // 2 - quit_text.get_width() // 2, 375))
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
                    return "quit"


def game_loop(): # Run one full session of the game (from start to collision).
    bird = Bird()
    pipes = [Pipe(config.WIDTH + i * 200) for i in range(3)]
    score = 0
    config.game_start = False  # Game flag is reset

    clock = pygame.time.Clock()

    while True:
        config.screen.blit(config.bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    config.game_start = True
                    bird.jump()

        bird.move()
        bird.draw(config.screen)

        for pipe in pipes[:]: # Update and draw pipes
            pipe.move()
            pipe.draw(config.screen)

            if not pipe.passed and pipe.x + config.pipe_img.get_width() < bird.x:
                pipe.passed = True
                score += 1

            if pipe.x < -config.pipe_img.get_width():
                pipes.remove(pipe)
                pipes.append(Pipe(config.WIDTH))

        if check_collision(bird, pipes):
            config.game_start = False
            return "game_over", score

        draw_score(config.screen, score, config.high_score)
        pygame.display.update()
        clock.tick(30)


def main():
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    while True:
        start_screen()
        state, score = game_loop()
        if state == "quit":
            break
        while True:
            action = end_screen(score)
            if action == "menu":
                break
            elif action == "restart":
                state, score = game_loop()
            elif action == "quit":
                confirm_quit()


    pygame.quit()

if __name__ == "__main__":
    main()
