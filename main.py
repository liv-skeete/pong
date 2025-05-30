# Pong 2.0
# With:
### throttle controled paddles 
### power-up
### momentum transfer
### random ball spawns
### AI template 
import pygame
import assets

# Constants
SCREEN_WDTH = 700
SCREEN_HGHT = 500
BALL_SIDE = 10
PADDLE_WDTH = 10
PADDLE_HGHT = 100 # Initial paddle height
ACCELERATION = 0.05 # Acc on ball at everybounce

# Setup
pygame.init() # Being a game "engine", it needs to be started
screen = pygame.display.set_mode((SCREEN_WDTH, SCREEN_HGHT))
font = pygame.font.SysFont("monospace", 36)

# Model Initialization
ball = assets.Ball(SCREEN_WDTH, SCREEN_HGHT, BALL_SIDE, ACCELERATION)
paddle1 = assets.Paddle(
  SCREEN_WDTH, 
  SCREEN_HGHT,
  PADDLE_WDTH, 
  PADDLE_HGHT, 
  0)
paddle2 = assets.Paddle(
  SCREEN_WDTH, 
  SCREEN_HGHT,
  PADDLE_WDTH, 
  PADDLE_HGHT, 
  SCREEN_WDTH-PADDLE_WDTH)

p1_score = 0
p2_score = 0
p1_throttle = assets.OFF
p1_powerup = assets.OFF
p2_throttle = assets.OFF
p2_powerup = assets.OFF

def p1ai(paddle1_y, ball_x, ball_y, ball_x_vel, ball_y_vel, p2_throttle, p2_powerup):
  # Tournament-compliant AI for left paddle (identical logic to p2ai)
  throttle = assets.OFF
  powerup = assets.OFF
  
  # Calculate paddle center for more accurate positioning
  paddle_center = paddle1_y + PADDLE_HGHT // 2
  
  if ball_x_vel < 0:  # Ball coming towards left paddle
    # Predict where ball will be when it reaches paddle
    time_to_reach = abs((ball_x - PADDLE_WDTH) / ball_x_vel)
    predicted_y = ball_y + ball_y_vel * time_to_reach
    
    # Handle wall bounces
    while predicted_y < 0 or predicted_y > SCREEN_HGHT:
      if predicted_y < 0:
        predicted_y = -predicted_y
      elif predicted_y > SCREEN_HGHT:
        predicted_y = 2 * SCREEN_HGHT - predicted_y
    
    # Calculate error between predicted ball position and paddle center
    error = predicted_y - paddle_center
    
    # Use deadzone to prevent oscillation (human-like behavior)
    if abs(error) > 12:  # Only move if significantly off target
      if error > 0:
        throttle = assets.DOWN
      else:
        throttle = assets.UP
    
    # Strategic powerup usage - only when ball is very close and we need the extra size
    if time_to_reach < 15 and abs(error) > 30:
      powerup = assets.ON
      
  else:  # Ball moving away - return to center position
    center_position = SCREEN_HGHT // 2
    error = center_position - paddle_center
    
    # Gradual return to center with deadzone
    if abs(error) > 25:
      if error > 0:
        throttle = assets.DOWN
      else:
        throttle = assets.UP
  
  return throttle, powerup

# Sample P2 AI:
def p2ai(paddle2_y, ball_x, ball_y, ball_x_vel, ball_y_vel, p1_throttle, p1_powerup):
  # Tournament-compliant AI with human-like behavior
  throttle = assets.OFF
  powerup = assets.OFF
  
  # Calculate paddle center for more accurate positioning
  paddle_center = paddle2_y + PADDLE_HGHT // 2
  
  if ball_x_vel > 0:  # Ball coming towards right paddle
    # Predict where ball will be when it reaches paddle
    time_to_reach = (SCREEN_WDTH - PADDLE_WDTH - ball_x) / ball_x_vel
    predicted_y = ball_y + ball_y_vel * time_to_reach
    
    # Handle wall bounces
    while predicted_y < 0 or predicted_y > SCREEN_HGHT:
      if predicted_y < 0:
        predicted_y = -predicted_y
      elif predicted_y > SCREEN_HGHT:
        predicted_y = 2 * SCREEN_HGHT - predicted_y
    
    # Calculate error between predicted ball position and paddle center
    error = predicted_y - paddle_center
    
    # Use deadzone to prevent oscillation (human-like behavior)
    if abs(error) > 12:  # Only move if significantly off target
      if error > 0:
        throttle = assets.DOWN
      else:
        throttle = assets.UP
    
    # Strategic powerup usage - only when ball is very close and we need the extra size
    if time_to_reach < 15 and abs(error) > 30:
      powerup = assets.ON
      
  else:  # Ball moving away - return to center position
    center_position = SCREEN_HGHT // 2
    error = center_position - paddle_center
    
    # Gradual return to center with deadzone
    if abs(error) > 25:
      if error > 0:
        throttle = assets.DOWN
      else:
        throttle = assets.UP
  
  return throttle, powerup
    

game = "on"
# Main loop
while game == "on":
  # Start of frame
  screen.fill((0,0,0)) # Clear frame
  pygame.time.wait(20) # Wait 20 milliseconds

  # CONTROLs
  # Manual controls
  pygame.event.pump()
  keys = pygame.key.get_pressed() 
  if keys[pygame.K_w]:
    p1_throttle = assets.UP #up
  elif keys[pygame.K_s]:
    p1_throttle = assets.DOWN #down
  else: # No input detected
    p1_throttle = assets.OFF
    
  if keys[pygame.K_e]:
    p1_powerup = assets.ON # use powerup
  else: # No input detected
    p1_powerup = assets.OFF
  
  # if keys[pygame.K_UP]:
  #   p2_throttle = assets.UP #up
  # if keys[pygame.K_DOWN]:
  #   p2_throttle = assets.DOWN #down
  # else:
    # p2_throttle = assets.OFF
  # if keys[pygame.K_LEFT]:
  #   p2_powerup = assets.ON #down
  # else:
  #   p2_powerup = assets.OFF
    
  # Dummy event to prevent the trinket from disconnecting 
  if keys[pygame.K_SPACE]:
    pass
    
  '''
  Each frame, p1_throttle and p2_throttle control if the paddle 
  will start to accelerate up or down or not at all. This is the 
  only way to control the paddles. 

  To use them programmatically, set it to assets.OFF to do nothing. 
  set it to assets.UP to go up, and set it to assets.DOWN to go down.
  '''
  # Player 1 AI
  p1_throttle, p1_powerup = p1ai(paddle1.y, ball.x, ball.y, ball.x_vel, ball.y_vel, p2_throttle, p2_powerup)
  
  # Player 2 AI
  p2_throttle, p2_powerup = p2ai(paddle2.y, ball.x, ball.y, ball.x_vel, ball.y_vel, p1_throttle, p1_powerup)


  
  # Updating model
  ball.update()
  paddle1.update(p1_throttle, p1_powerup)
  paddle2.update(p2_throttle, p2_powerup)

  # Score keeping
  if ball.x < 0: # Reached left & Not caught
    p2_score += 1
    ball.reset()
  if ball.x + BALL_SIDE > SCREEN_WDTH: # Reached right & not caught
    p1_score += 1
    ball.reset()
  if p1_score == 5:
    game = "Player 1, left, wins"  # Ends game, also end msg
  if p2_score == 5:
    game = "Player 2, right, wins" # Ends game, also end msg

  # Create rect objects for collision
  ball_rect = ball.rect()
  # Paddle collision with ball
  if paddle1.rect().colliderect(ball_rect):
    ball.hori_bounce(paddle1.vel)
  if paddle2.rect().colliderect(ball_rect):
    ball.hori_bounce(paddle2.vel)

  # RENDERING
  # Ball
  ball.render(screen)
  paddle1.render(screen)
  paddle2.render(screen)

  # Scores
  screen.blit(font.render(str(p1_score), 1, assets.WHITE), (3*SCREEN_WDTH//8, 50))
  screen.blit(font.render(str(p2_score), 1, assets.WHITE), (5*SCREEN_WDTH//8, 50))

  pygame.display.update()  
  # End of frame

print(game)
pygame.quit()