import pygame
import sys
import time

pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Difficulty Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
DARKGRAY = (90, 90, 90)

# Game settings
paddle_width, paddle_height = 15, 200
BALL_SIZE = 20
ball_speed_x = 5
ball_speed_y = 5
paddle_speed1 = 5
paddle_speed2 = 2

# High Score
high_score_time = 0

# Game objects
player_paddle = pygame.Rect(20, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ai_paddle = pygame.Rect(WIDTH - 35, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Score
player_score = 0
ai_score = 0
winning_score = 10

# Fonts
font = pygame.font.SysFont(None, 50)
FONT = pygame.font.SysFont(None, 20)

# ----- DIFFICULTY SELECTION -----
def difficulty_screen():
    global ball_speed_x, ball_speed_y, paddle_speed2, player_score, ai_score
    player_score = 0
    ai_score = 0

    button_w, button_h = 250, 50
    easy_btn = pygame.Rect(WIDTH // 2 - button_w // 2, 250, button_w, button_h)
    medium_btn = pygame.Rect(WIDTH // 2 - button_w // 2, 320, button_w, button_h)
    hard_btn = pygame.Rect(WIDTH // 2 - button_w // 2, 390, button_w, button_h)
    impossible_btn = pygame.Rect(WIDTH // 2 - button_w // 2, 460, button_w, button_h)

    difficulty_selected = False
    while not difficulty_selected:
        screen.fill(BLACK)
        title = font.render("Choose Difficulty: Click", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

        for rect, text in [(easy_btn, "Easy"), (medium_btn, "Medium"), (hard_btn, "Hard"), (impossible_btn, "Impossible")]:
            mouse_pos = pygame.mouse.get_pos()
            color = DARKGRAY if rect.collidepoint(mouse_pos) else GRAY
            pygame.draw.rect(screen, color, rect)
            txt_surf = font.render(text, True, BLACK)
            txt_rect = txt_surf.get_rect(center=rect.center)
            screen.blit(txt_surf, txt_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_btn.collidepoint(event.pos):
                    paddle_speed2 = 2
                    ball_speed_x = 5
                    ball_speed_y = 5
                    difficulty_selected = True
                elif medium_btn.collidepoint(event.pos):
                    paddle_speed2 = 3
                    ball_speed_x = 6
                    ball_speed_y = 6
                    difficulty_selected = True
                elif hard_btn.collidepoint(event.pos):
                    paddle_speed2 = 5
                    ball_speed_x = 7
                    ball_speed_y = 7
                    difficulty_selected = True
                elif impossible_btn.collidepoint(event.pos):
                    paddle_speed2 = 7
                    ball_speed_x = 8
                    ball_speed_y = 8
                    difficulty_selected = True

# ----- Game Functions -----
def reset_ball():
    global ball_speed_x
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1
   

def draw(seconds, high_score_time):
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, player_paddle)
    pygame.draw.rect(screen, GREEN, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    player_text = font.render(str(player_score), True, GREEN)
    ai_text = font.render(str(ai_score), True, GREEN)
    screen.blit(player_text, (WIDTH // 4, 20))
    screen.blit(ai_text, (WIDTH * 3 // 4, 20))

    timer_surf = FONT.render(f"Time: {seconds} seconds", True, WHITE)
    screen.blit(timer_surf, (20, 20))

    high_score_surf = FONT.render(f"Best Time: {high_score_time} seconds", True, WHITE)
    screen.blit(high_score_surf, (20, 50))

    pygame.display.update()

def ai_move():
    if ai_paddle.centery < ball.centery:
        ai_paddle.y += paddle_speed2
    elif ai_paddle.centery > ball.centery:
        ai_paddle.y -= paddle_speed2

    ai_paddle.top = max(ai_paddle.top, 0)
    ai_paddle.bottom = min(ai_paddle.bottom, HEIGHT)

def game_loop():
    global player_score, ai_score, ball_speed_x, ball_speed_y, high_score_time

    player_paddle.y = HEIGHT // 2 - paddle_height // 2
    ai_paddle.y = HEIGHT // 2 - paddle_height // 2
    ball.center = (WIDTH // 2, HEIGHT // 2)
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        # Update high score time if player is still playing
        if seconds > high_score_time:
            high_score_time = seconds

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_paddle.y -= paddle_speed1
        if keys[pygame.K_s]:
            player_paddle.y += paddle_speed1

        player_paddle.top = max(player_paddle.top, 0)
        player_paddle.bottom = min(player_paddle.bottom, HEIGHT)

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(player_paddle) and ball_speed_x < 0:
            ball_speed_x *= -1
        if ball.colliderect(ai_paddle) and ball_speed_x > 0:
            ball_speed_x *= -1

        if ball.left <= 0:
            ai_score += 1
            reset_ball()
        if ball.right >= WIDTH:
            player_score += 1
            reset_ball()

        if player_score >= winning_score or ai_score >= winning_score:
            winner = "Player" if player_score >= winning_score else "AI"
            win_text = font.render(f"{winner} wins! Time {seconds}", True, WHITE)
            screen.fill(BLACK)
            screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(8000)
            running = False

        ai_move()
        draw(seconds, high_score_time)
        clock.tick(60)

# ----- MAIN LOOP -----
while True:
    difficulty_screen()
    pygame.event.clear()
    game_loop()
