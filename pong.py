import pygame
import sys

pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Difficulty Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Game settings
paddle_width, paddle_height = 15, 200
BALL_SIZE = 20
ball_speed_x = 5  # Default (may get overwritten by difficulty)
ball_speed_y = 5
paddle_speed1 = 5
paddle_speed2 = 2

# Game objects
player_paddle = pygame.Rect(20, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ai_paddle = pygame.Rect(WIDTH - 35, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Score
player_score = 0
ai_score = 0
winning_score = 10

font = pygame.font.SysFont(None, 50)

# ----- DIFFICULTY SELECTION -----
def difficulty_screen():
    global ball_speed_x, ball_speed_y, paddle_speed2, player_score, ai_score
    player_score = 0
    ai_score = 0
    difficulty_selected = False
    while not difficulty_selected:
        screen.fill(BLACK)
        title = font.render("Choose Difficulty", True, WHITE)
        easy = font.render("Press E for Easy", True, WHITE)
        medium = font.render("Press M for Medium", True, WHITE)
        hard = font.render("Press H for Hard", True, WHITE)
        impossible = font.render("Press I for Impossible", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        screen.blit(easy, (WIDTH // 2 - easy.get_width() // 2, 250))
        screen.blit(medium, (WIDTH // 2 - medium.get_width() // 2, 320))
        screen.blit(hard, (WIDTH // 2 - hard.get_width() // 2, 390))
        screen.blit(impossible, (WIDTH // 2 - impossible.get_width() // 2, 460))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    paddle_speed2 = 2
                    ball_speed_x = 4
                    ball_speed_y = 4
                    difficulty_selected = True
                elif event.key == pygame.K_m:
                    paddle_speed2 = 3
                    ball_speed_x = 5
                    ball_speed_y = 5
                    difficulty_selected = True
                elif event.key == pygame.K_h:
                    paddle_speed2 = 5
                    ball_speed_x = 6
                    ball_speed_y = 6
                    difficulty_selected = True
                elif event.key == pygame.K_i:
                    paddle_speed2 = 8
                    ball_speed_x = 7
                    ball_speed_y = 7
                    difficulty_selected = True

# ----- Game Functions -----
def reset_ball():
    global ball_speed_x
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, player_paddle)
    pygame.draw.rect(screen, GREEN, ai_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    player_text = font.render(str(player_score), True, GREEN)
    ai_text = font.render(str(ai_score), True, GREEN)
    screen.blit(player_text, (WIDTH // 4, 20))
    screen.blit(ai_text, (WIDTH * 3 // 4, 20))

    pygame.display.update()

def ai_move():
    if ai_paddle.centery < ball.centery:
        ai_paddle.y += paddle_speed2
    elif ai_paddle.centery > ball.centery:
        ai_paddle.y -= paddle_speed2

    ai_paddle.top = max(ai_paddle.top, 0)
    ai_paddle.bottom = min(ai_paddle.bottom, HEIGHT)

# ---- RUN DIFFICULTY SELECTION FIRST ----
difficulty_screen()

# ---- Game Loop ----
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_paddle.y -= paddle_speed1
    if keys[pygame.K_s]:
        player_paddle.y += paddle_speed1

    # Stay on screen
    player_paddle.top = max(player_paddle.top, 0)
    player_paddle.bottom = min(player_paddle.bottom, HEIGHT)

    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Bounce
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    if ball.colliderect(player_paddle) and ball_speed_x < 0:
        ball_speed_x *= -1
    if ball.colliderect(ai_paddle) and ball_speed_x > 0:
        ball_speed_x *= -1

    # Score
    if ball.left <= 0:
        ai_score += 1
        reset_ball()
    if ball.right >= WIDTH:
        player_score += 1
        reset_ball()

    if player_score >= winning_score or ai_score >= winning_score:
        winner = "Player" if player_score >= winning_score else "AI"
        win_text = font.render(f"{winner} wins!", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    ai_move()
    draw()
    clock.tick(60)

pygame.quit()
sys.exit()
