# This file contains the classes for Ball & Paddle

import pygame
import random

# Constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SPEED_CAP = 3.8
ACCELERATION = 0.23

# Throttle controls
OFF = 0
UP = -1
DOWN = 1
ON = 1

# Helper functions
def rand_nonzero(floor, ceil):
  result = 0
  while result == 0:
    result = random.randint(floor, ceil)
  return result


# Classes
class Ball:

  def __init__(self, SCREEN_WDTH, SCREEN_HGHT, BALL_SIDE, ACCELERATION):
    self.SCREEN_WDTH = SCREEN_WDTH
    self.SCREEN_HGHT = SCREEN_HGHT
    self.BALL_SIDE = BALL_SIDE
    self.ACCELERATION = ACCELERATION
    self.reset()

  def reset(self):
    'For spawning & respawning'
    self.x = self.SCREEN_WDTH // 2 - self.BALL_SIDE // 2
    self.y = self.SCREEN_HGHT // 2 - self.BALL_SIDE // 2
    self.x_vel = rand_nonzero(-3, 3)
    self.y_vel = rand_nonzero(-1, 1) * (3**2 + 1 - self.x_vel**2)**0.5
    self.spawn_timer = 25

  def rect(self):
    'Returns a Rect object to represent its hitbox'
    return pygame.Rect(self.x, self.y, self.BALL_SIDE, self.BALL_SIDE)

  def update(self):
    'Updates location based on velocity'
    if self.spawn_timer == 0:
      self.x += self.x_vel
      self.y += self.y_vel
    else:  # Countdown for visibility
      self.spawn_timer -= 1

    # Checks for top & bottom borders:
    if self.y + self.BALL_SIDE > self.SCREEN_HGHT or self.y < 0: # Reached top or bottom
      self.vert_bounce()

  def vert_bounce(self):
    self.y_vel *= -(1 + self.ACCELERATION)  # Speed up on bounce
    self.x_vel *= (1 + self.ACCELERATION)  # Speed up on bounce
    
  def hori_bounce(self, momentum):
    # Bounce horizontally
    # Transfer some vertical momentum from paddle to ball
    self.x_vel *= -(1 + self.ACCELERATION)  # Speed up on bounce
    self.y_vel += 4*momentum/7 # Can't do half, in case y_vel zeroes out
    self.y_vel *=  (1 + self.ACCELERATION) 

  def render(self, surf):
    pygame.draw.rect(surf, WHITE, self.rect())


class Paddle:
  def __init__(self, SCREEN_WDTH, SCREEN_HGHT, PADDLE_WIDTH, PADDLE_HGHT, X):
    self.SCREEN_WDTH = SCREEN_WDTH
    self.SCREEN_HGHT = SCREEN_HGHT
    self.PADDLE_WIDTH = PADDLE_WIDTH
    self.paddle_hght = PADDLE_HGHT
    self.X = X
    self.reset()

  def reset(self):
    'For spawning & respawning'
    self.y = self.SCREEN_HGHT//2-self.paddle_hght//2 # centered
    self.vel = 0
    self.throttle = OFF
    self.extend = 101 # power up timer
    self.speed = 101 # power up timer

  def rect(self):
    'Returns a Rect object to represent its hitbox'
    return pygame.Rect(self.X, self.y, self.PADDLE_WIDTH, self.paddle_hght)

  def update(self, new_throttle, extendon=OFF):
    'Updates location based on velocity'
    if new_throttle == OFF:
      self.vel *= 0.5 # Will slow to a stop
    else:
      self.vel += new_throttle*ACCELERATION

    self.vel = max(self.vel, -SPEED_CAP) # Cap on speed
    self.vel = min(self.vel, SPEED_CAP) # Cap on speed
    self.y += self.vel # Update according to velocity
    self.y = max(self.y, 0) # Top border
    self.y = min(self.y, self.SCREEN_HGHT - self.paddle_hght) # Bottom border
    
    # Powerup:
    if extendon == ON and self.extend == 101: # Turn on
      self.extend -= 1
      self.paddle_hght *= 2
    if self.extend<=100: # Decrement every round, doubles as flag
      self.extend -= 1
    if self.extend == 0: # Timer runs out
      self.paddle_hght /= 2

  def render(self, surf):
    pygame.draw.rect(surf, RED if 0 < self.extend <= 100 else WHITE, self.rect())