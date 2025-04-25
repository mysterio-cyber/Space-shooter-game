import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Game states
RUNNING = "running"
GAME_OVER = "game over"
game_state = RUNNING

# Starfield
stars = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT)} for _ in range(100)]

# Game variables
def init_game():
    return {
        "player_x": WIDTH // 2,
        "player_y": HEIGHT - 100,
        "player_speed": 5,
        "bullets": [],
        "enemies": [],
        "score": 0,
        "lives": 5
    }

game = init_game()

# Draw rocket
def draw_rocket(x, y):
    pygame.draw.rect(screen, (192, 192, 192), (x + 10, y + 20, 30, 60), border_radius=15)
    pygame.draw.polygon(screen, (255, 0, 0), [(x + 10, y + 20), (x + 40, y + 20), (x + 25, y)])
    pygame.draw.circle(screen, (0, 191, 255), (x + 25, y + 40), 6)
    pygame.draw.circle(screen, (255, 255, 255), (x + 25, y + 40), 6, 1)
    pygame.draw.polygon(screen, (255, 0, 0), [(x + 10, y + 80), (x, y + 90), (x + 10, y + 90)])
    pygame.draw.polygon(screen, (255, 0, 0), [(x + 40, y + 80), (x + 50, y + 90), (x + 40, y + 90)])
    pygame.draw.polygon(screen, (255, 140, 0), [(x + 25, y + 80), (x + 15, y + 100), (x + 35, y + 100)])

# Draw custom bullet
def draw_bullet(bullet):
    pygame.draw.rect(screen, (0, 255, 255), bullet)
    pygame.draw.line(screen, (0, 255, 0), (bullet.x, bullet.y), (bullet.x + bullet.width, bullet.y), 1)

# Draw custom enemy
def draw_enemy(x, y):
    body = pygame.Rect(x, y, 40, 40)
    pygame.draw.ellipse(screen, (255, 50, 50), body)
    pygame.draw.polygon(screen, (200, 0, 0), [(x, y), (x + 20, y - 20), (x + 40, y)])
    pygame.draw.circle(screen, (0, 0, 0), (x + 20, y + 20), 5)
    return body

# Starfield background
def draw_background():
    screen.fill((5, 5, 20))
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (star["x"], star["y"]), 1)
        star["y"] += 1
        if star["y"] > HEIGHT:
            star["y"] = 0
            star["x"] = random.randint(0, WIDTH)

# Spawn enemy
def spawn_enemy():
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-100, -40)
    game["enemies"].append([x, y])

# Restart game
def restart_game():
    global game_state, game
    game = init_game()
    game_state = RUNNING


# Main game loop
running = True
while running:
    clock.tick(60)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == RUNNING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and game["player_x"] > 0:
            game["player_x"] -= game["player_speed"]
        if keys[pygame.K_RIGHT] and game["player_x"] < WIDTH - 50:
            game["player_x"] += game["player_speed"]
        if keys[pygame.K_SPACE]:
            if len(game["bullets"]) < 5:
                game["bullets"].append(pygame.Rect(game["player_x"] + 22, game["player_y"] + 10, 6, 20))

        draw_rocket(game["player_x"], game["player_y"])

        # Bullets
        for bullet in game["bullets"][:]:
            bullet.y -= 10
            draw_bullet(bullet)
            if bullet.y < -20:
                game["bullets"].remove(bullet)

        # Enemies
        if random.randint(1, 60) == 1:
            spawn_enemy()

        player_rect = pygame.Rect(game["player_x"] + 10, game["player_y"] + 20, 30, 60)

        for enemy_pos in game["enemies"][:]:
            enemy_pos[1] += 2
            enemy_rect = draw_enemy(enemy_pos[0], enemy_pos[1])

            if enemy_rect.colliderect(player_rect):
                game["enemies"].remove(enemy_pos)
                game["lives"] -= 1
                continue

            if enemy_pos[1] > HEIGHT:
                game["enemies"].remove(enemy_pos)
                game["lives"] -= 0
                continue

            for bullet in game["bullets"][:]:
                if enemy_rect.colliderect(bullet):
                    game["enemies"].remove(enemy_pos)
                    game["bullets"].remove(bullet)
                    game["score"] += 1
                    break

        # HUD
        score_text = font.render(f"Score: {game['score']}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {game['lives']}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 130, 10))
        if game["lives"] <= 0:
            game_state = GAME_OVER

    elif game_state == GAME_OVER:
        over_text = font.render("GAME OVER  - press R to restart", True, (255, 255, 0))
        screen.blit(over_text, (WIDTH // 2 - 200, HEIGHT // 2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            restart_game()

    pygame.display.flip()

pygame.quit()
sys.exit()
