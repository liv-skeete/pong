class Paddle:
    def __init__(self, SCREEN_WDTH, SCREEN_HGHT, PADDLE_WIDTH, PADDLE_HGHT, X):
        self.SCREEN_WDTH = SCREEN_WDTH
        self.SCREEN_HGHT = SCREEN_HGHT
        self.PADDLE_WIDTH = PADDLE_WIDTH
        self.paddle_hght = PADDLE_HGHT
        self.X = X
        self.reset()

    def reset(self):
        self.y = self.SCREEN_HGHT//2 - self.paddle_hght//2
        self.vel = 0
        self.throttle = OFF
        self.extend = 101
        self.speed = 101

    def update(self, new_throttle, extendon=OFF):
        # Smooth acceleration with momentum consideration
        if new_throttle != self.throttle:
            self.vel *= 0.7  # Immediate response to throttle changes
            
        self.vel += new_throttle * ACCELERATION
        self.vel = max(min(self.vel, SPEED_CAP), -SPEED_CAP)
        
        # Apply movement with velocity damping
        self.y += self.vel
        self.vel *= 0.95 if new_throttle == OFF else 0.99
        
        # Boundary checks
        self.y = max(0, min(self.y, self.SCREEN_HGHT - self.paddle_hght))