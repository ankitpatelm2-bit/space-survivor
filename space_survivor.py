
import pygame
import random
import os

pygame.init()

WIDTH = 600
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE SURVIVOR")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (40, 210, 255)

font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 65)

player = pygame.Rect(270, 580, 60, 70)

player_speed = 7

asteroids = []

score = 0
game_over = False
game_started = False

highscore_file = "highscore.txt"

if os.path.exists(highscore_file):
    with open(highscore_file, "r") as file:
        high_score = int(file.read())
else:
    high_score = 0

stars = []

for i in range(80):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])


def draw_spaceship(screen, rect):
    x, y, w, h = rect

    pygame.draw.polygon(screen, (255, 120, 20), [
        (x + w * 0.35, y + h * 0.72),
        (x + w * 0.5, y + h * 1.05),
        (x + w * 0.65, y + h * 0.72)
    ])

    pygame.draw.polygon(screen, (255, 220, 70), [
        (x + w * 0.43, y + h * 0.72),
        (x + w * 0.5, y + h * 0.92),
        (x + w * 0.57, y + h * 0.72)
    ])

    pygame.draw.polygon(screen, (180, 195, 215), [
        (x + w * 0.5, y),
        (x + w * 0.72, y + h * 0.55),
        (x + w * 0.65, y + h * 0.85),
        (x + w * 0.35, y + h * 0.85),
        (x + w * 0.28, y + h * 0.55)
    ])

    pygame.draw.polygon(screen, (70, 120, 190), [
        (x + w * 0.3, y + h * 0.48),
        (x, y + h * 0.85),
        (x + w * 0.35, y + h * 0.75)
    ])

    pygame.draw.polygon(screen, (70, 120, 190), [
        (x + w * 0.7, y + h * 0.48),
        (x + w, y + h * 0.85),
        (x + w * 0.65, y + h * 0.75)
    ])

    pygame.draw.ellipse(
        screen, (40, 210, 255),
        (x + w * 0.39, y + h * 0.2, w * 0.22, h * 0.3)
    )

    pygame.draw.ellipse(
        screen, (180, 245, 255),
        (x + w * 0.44, y + h * 0.24, w * 0.08, h * 0.12)
    )


def draw_asteroid(screen, rect):
    x, y, w, h = rect

    points = [
        (x + w * 0.50, y),
        (x + w * 0.78, y + h * 0.12),
        (x + w, y + h * 0.42),
        (x + w * 0.83, y + h * 0.78),
        (x + w * 0.55, y + h),
        (x + w * 0.20, y + h * 0.85),
        (x, y + h * 0.55),
        (x + w * 0.12, y + h * 0.20)
    ]

    pygame.draw.polygon(screen, (105, 95, 85), points)
    pygame.draw.polygon(screen, (155, 140, 120), points, 3)

    pygame.draw.circle(
        screen, (65, 60, 55),
        (int(x + w * 0.35), int(y + h * 0.35)),
        max(2, int(w * 0.10))
    )

    pygame.draw.circle(
        screen, (75, 68, 60),
        (int(x + w * 0.68), int(y + h * 0.62)),
        max(2, int(w * 0.13))
    )

    pygame.draw.circle(
        screen, (125, 115, 100),
        (int(x + w * 0.35), int(y + h * 0.35)),
        max(2, int(w * 0.10)), 2
    )


def draw_stars():
    for star in stars:
        pygame.draw.circle(
            screen,
            WHITE,
            (star[0], star[1]),
            star[2]
        )

        star[1] += star[2]

        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)


def reset_game():
    global player, asteroids, score, game_over

    player = pygame.Rect(270, 580, 60, 70)
    asteroids = []
    score = 0
    game_over = False


running = True

while running:

    clock.tick(60)

    screen.fill((5, 5, 25))

    draw_stars()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if not game_started and event.key == pygame.K_SPACE:
                game_started = True

            elif game_over and event.key == pygame.K_r:
                reset_game()

    if not game_started:

        title = big_font.render("SPACE SURVIVOR", True, BLUE)
        instruction = font.render("Press SPACE to Start", True, WHITE)
        controls = small_font.render("Use LEFT and RIGHT arrow keys", True, WHITE)

        screen.blit(title, (75, 230))
        screen.blit(instruction, (155, 330))
        screen.blit(controls, (130, 390))

    elif not game_over:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed

        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed

        spawn_rate = max(12, 35 - score // 5)

        if random.randint(1, spawn_rate) == 1:

            size = random.randint(35, 55)

            asteroid = {
                "rect": pygame.Rect(
                    random.randint(0, WIDTH - size),
                    -size,
                    size,
                    size
                ),
                "speed": random.randint(3, 6) + score // 10
            }

            asteroids.append(asteroid)

        for asteroid in asteroids[:]:

            asteroid["rect"].y += asteroid["speed"]

            draw_asteroid(screen, asteroid["rect"])

            if asteroid["rect"].top > HEIGHT:
                asteroids.remove(asteroid)
                score += 1

            if player.colliderect(asteroid["rect"]):
                game_over = True

        draw_spaceship(screen, player)

        score_text = font.render("Score: " + str(score), True, WHITE)
        high_text = small_font.render(
            "High Score: " + str(max(score, high_score)),
            True,
            WHITE
        )

        screen.blit(score_text, (10, 10))
        screen.blit(high_text, (10, 55))

        if score > high_score:
            high_score = score

            with open(highscore_file, "w") as file:
                file.write(str(high_score))

    else:

        over_text = big_font.render("GAME OVER", True, (255, 60, 60))
        final_score = font.render(
            "Your Score: " + str(score), True, WHITE
        )
        best_score = font.render(
            "High Score: " + str(high_score), True, WHITE
        )
        restart_text = small_font.render(
            "Press R to Restart", True, BLUE
        )

        screen.blit(over_text, (130, 230))
        screen.blit(final_score, (200, 330))
        screen.blit(best_score, (190, 385))
        screen.blit(restart_text, (200, 460))

    pygame.display.update()

pygame.quit()

