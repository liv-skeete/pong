# Boilerplate
import pygame
import random

pygame.init()  # Initialize pygame modules

# Game configuration constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 50
PADDLE_ACCEL = 0.7
PADDLE_FRICTION = 0.92
BALL_SIZE = 10
INITIAL_BALL_SPEED = 3
WINNING_SCORE = 5

# Initialize display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")

# Initialize game state
player1_score = 0
player2_score = 0
game_state = "playing"

player1_x = 0
player1_y = 100
player2_x = SCREEN_WIDTH - PADDLE_WIDTH
player2_y = 100

# Initialize paddle velocities and counters
player1_vel = 0
player2_vel = 0

# Model
ball_x = 50
ball_y = 60
ball_side = 10
ball_x_vel = +3
ball_y_vel = +3

game = "on"

def reset_ball():
    # Reset ball to center with random direction
    global ball_x, ball_y, ball_x_vel, ball_y_vel
    ball_x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
    ball_y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
    # Randomly choose direction for the ball's horizontal velocity
    ball_x_vel = INITIAL_BALL_SPEED * random.choice([-1, 1])
    ball_y_vel = INITIAL_BALL_SPEED

def draw_score():
    # Render player scores on screen
    font = pygame.font.Font(None, 74)
    text = font.render(str(player1_score), True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH//4 - text.get_width()//2, 10))
    text = font.render(str(player2_score), True, (255, 255, 255))
    screen.blit(text, (3*SCREEN_WIDTH//4 - text.get_width()//2, 10))

def draw_center_line():
    # Draw dashed center line
    for y in range(0, SCREEN_HEIGHT, 20):
        if y % 40 == 0:
            pygame.draw.line(screen, (255,255,255), (SCREEN_WIDTH//2, y), (SCREEN_WIDTH//2, y+10), 2)

# Main game loop
# Game mode variables
player1_ai = False
player2_ai = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    screen.fill((0, 0, 0))  # Clear screen with black

    if game_state == "playing":
        keys = pygame.key.get_pressed()

        # Player 1 controls
        if not player1_ai:
            # Player 1 manual controls (W/S keys) with acceleration
            if keys[pygame.K_w]:
                player1_vel -= PADDLE_ACCEL
            if keys[pygame.K_s]:
                player1_vel += PADDLE_ACCEL
        else:
            # Predictive AI for Player 1
            time_to_reach = abs((player1_x - ball_x) / ball_x_vel)
            predicted_y = ball_y + ball_y_vel * time_to_reach
            # Account for wall collisions
            num_bounces = int(abs(predicted_y) // SCREEN_HEIGHT)
            predicted_y = abs(predicted_y) % SCREEN_HEIGHT
            if num_bounces % 2 == 1:
                predicted_y = SCREEN_HEIGHT - predicted_y
            if predicted_y < player1_y + PADDLE_HEIGHT / 2:
                player1_vel -= PADDLE_ACCEL
            elif predicted_y > player1_y + PADDLE_HEIGHT / 2:
                player1_vel += PADDLE_ACCEL
            else:
                player1_vel = 0

            # Apply friction and velocity
            player1_vel *= PADDLE_FRICTION
            player2_vel *= PADDLE_FRICTION
            player1_y += player1_vel
            player2_y += player2_vel

        # Player 2 controls
        if not player2_ai:
            # Player 2 manual controls (Up/Down arrows) with acceleration
            if keys[pygame.K_UP]:
                player2_vel -= PADDLE_ACCEL
            if keys[pygame.K_DOWN]:
                player2_vel += PADDLE_ACCEL
        else:
            # Predictive AI for Player 2
            time_to_reach = abs((player2_x - ball_x) / ball_x_vel)
            predicted_y = ball_y + ball_y_vel * time_to_reach
            num_bounces = int(abs(predicted_y) // SCREEN_HEIGHT)
            predicted_y = abs(predicted_y) % SCREEN_HEIGHT
            if num_bounces % 2 == 1:
                predicted_y = SCREEN_HEIGHT - predicted_y
            if predicted_y < player2_y + PADDLE_HEIGHT / 2:
                player2_vel -= PADDLE_ACCEL
            elif predicted_y > player2_y + PADDLE_HEIGHT / 2:
                player2_vel += PADDLE_ACCEL
            else:
                player2_vel = 0

        # Apply friction and velocity
        player1_vel *= PADDLE_FRICTION
        player2_vel *= PADDLE_FRICTION
        player1_y += player1_vel
        player2_y += player2_vel

        # Update ball position
        ball_x += ball_x_vel
        ball_y += ball_y_vel

        # Vertical wall collisions (top/bottom)
        if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - BALL_SIZE:
            ball_y_vel *= -1

        # Create rect objects for collision detection
        ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
        paddle1_rect = pygame.Rect(player1_x, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        paddle2_rect = pygame.Rect(player2_x, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT)

        # Paddle collisions
        if ball_rect.colliderect(paddle1_rect) or ball_rect.colliderect(paddle2_rect):
            ball_x_vel *= -1
            ball_x_vel *= 1.1
            ball_y_vel *= 1.1

        # Score points and reset ball
        if ball_x <= 0:
            player2_score += 1
            reset_ball()
        if ball_x >= SCREEN_WIDTH - BALL_SIZE:
            player1_score += 1
            reset_ball()

        # Check winning condition
        if player1_score >= WINNING_SCORE or player2_score >= WINNING_SCORE:
            game_state = "game_over"

        # Boundary checking for paddles
        player1_y = max(0, min(player1_y, SCREEN_HEIGHT - PADDLE_HEIGHT))
        player2_y = max(0, min(player2_y, SCREEN_HEIGHT - PADDLE_HEIGHT))

    # Game over state
    if game_state == "game_over":
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 40))
        winner = "Player 1" if player1_score > player2_score else "Player 2"
        text = font.render(f"{winner} Wins!", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 + 20))
        text = font.render("Press R to restart", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 + 80))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player1_score = 0
            player2_score = 0
            game_state = "playing"
            reset_ball()

    # Draw game elements
    draw_center_line()
    draw_score()
    pygame.draw.rect(screen, (255, 255, 255), (player1_x, player1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (player2_x, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (ball_x, ball_y, BALL_SIZE, BALL_SIZE))

    pygame.display.update()
    pygame.time.wait(20)