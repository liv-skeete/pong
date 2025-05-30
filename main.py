def p1ai(paddle1_y, ball_x, ball_y, ball_x_vel, ball_y_vel):
    throttle = assets.OFF
    powerup = assets.OFF
    
    if ball_x_vel < 0:
        # Calculate time to reach paddle including acceleration
        time_to_reach = 0
        current_x = ball_x
        current_x_vel = ball_x_vel
        while current_x > PADDLE_WDTH and abs(current_x_vel) > 0.1:
            time_to_reach += 1
            current_x += current_x_vel
            current_x_vel *= (1 + assets.ACCELERATION)
        
        # Predict final position with momentum
        predicted_y = ball_y + (ball_y_vel * time_to_reach)
        predicted_y += 0.5 * (assets.ACCELERATION * ball_y_vel) * (time_to_reach**2)
        
        # Account for bounces
        predicted_y = predicted_y % (2 * SCREEN_HGHT)
        if predicted_y > SCREEN_HGHT:
            predicted_y = 2 * SCREEN_HGHT - predicted_y
        
        # Calculate ideal position with lead
        target_y = predicted_y - (paddle1.vel * time_to_reach * 0.7)
        target_y = max(0, min(target_y, SCREEN_HGHT - PADDLE_HGHT))
        
        # Determine movement with velocity matching
        position_diff = target_y - (paddle1_y + PADDLE_HGHT/2)
        if abs(position_diff) > 5:  # Deadzone to prevent oscillation
            throttle = assets.DOWN if position_diff > 0 else assets.UP
            
    return throttle, powerup