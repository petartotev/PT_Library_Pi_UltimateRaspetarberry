from machine import Pin, ADC
import RGB1602
import utime
import random

# LCD
lcd = RGB1602.RGB1602(16, 2)
lcd.setRGB(64, 128, 64)

# Joystick
xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
button = Pin(16, Pin.IN, Pin.PULL_UP)

# Game Props
car_x = 0
car_y = 0
car_prev_x = 0
car_prev_y = 0

obstacles = []
obstacle_spawn_timer = 0
obstacle_spawn_interval = 30  # Longer spawn interval

score = 0
score_target = 3  # Adjusted score target for faster testing
level = 1
level_target = 3

def move_car():
    global car_x, car_y, car_prev_x, car_prev_y
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()

    car_prev_x, car_prev_y = car_x, car_y

    if xValue <= 600 and car_x > 0:  # left
        car_x -= 1
    elif xValue >= 60000 and car_x < 13:  # right
        car_x += 1

    if yValue <= 600:  # up
        car_y = 0
    elif yValue >= 60000:  # down
        car_y = 1

def draw_car():
    global car_x, car_y, car_prev_x, car_prev_y
    # Only clear the previous car position on the row where it was located
    if car_prev_y == 0:
        lcd.setCursor(car_prev_x, car_prev_y)
        lcd.printout("    ")  # Clear previous position first
    else:
        lcd.setCursor(car_prev_x, car_prev_y)
        lcd.printout("    ")

    # Draw the car in the new position
    lcd.setCursor(car_x, car_y)
    lcd.printout("(||)")

def spawn_obstacle():
    global obstacle_spawn_timer
    if obstacle_spawn_timer <= 0:
        size = random.randint(3, 7)  # Adjusted obstacle size
        y_pos = random.choice([0, 1])
        if not any(obs for obs in obstacles if obs["y"] == y_pos and 12 <= obs["x"] <= 15):  # Ensure space between obstacles
            obstacles.append({"x": 15, "y": y_pos, "size": size})
            obstacle_spawn_timer = obstacle_spawn_interval + random.randint(20, 40)  # Increased interval
    else:
        obstacle_spawn_timer -= 1

def move_obstacles():
    global obstacles, score
    for obs in obstacles[:]:
        # Clear previous obstacle position on the correct row
        for i in range(obs["size"] + 1):  # Adding +1 to ensure clearing the tail
            clear_x = obs["x"] + i
            if 0 <= clear_x < 16:
                # Clear on the correct row where the obstacle is
                lcd.setCursor(clear_x, obs["y"])  # Only clear on the row where the obstacle exists
                lcd.printout(" ")

        # Move the obstacle
        obs["x"] -= 1
        if obs["x"] + obs["size"] >= 0:
            # Draw the obstacle on the correct row
            for i in range(obs["size"] + 1):
                lcd.setCursor(obs["x"] + i, obs["y"])
                lcd.printout("|")
        else:
            obstacles.remove(obs)
            score += 1
            lcd.clear()

def check_collision():
    for obs in obstacles:
        if car_y == obs["y"] and any(x in range(obs["x"], obs["x"] + obs["size"]) for x in range(car_x, car_x + 4)):
            return True
    return False

def print_game_stats():
    lcd.setCursor(14, 0)
    lcd.printout(f"L{level}")
    lcd.setCursor(14, 1)
    lcd.printout(f"{score:02}")

def play_game_intro_animation():
    lcd.clear()
    utime.sleep(1)
    lcd.setRGB(128, 0, 0)
    lcd.setCursor(0, 0)
    lcd.printout(")               ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("|)              ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("||)             ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("(||)            ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout(" (||)           ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("  (||)          ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("   (||)         ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("    (||)        ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("     (||)       ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      (||)      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      R(||)     ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      RA(||)    ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      RAC(||)   ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      RACE(||)  ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      RACE (||) ")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      RACE  (||)")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      RACE   (||")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      RACE    (|")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      RACE     (")
    utime.sleep(0.15)
    lcd.setCursor(0, 0)
    lcd.printout("      RACE      ")
    utime.sleep(1)

    lcd.setCursor(0, 1)
    lcd.printout("               (")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("              (|")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("             (||")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("            (||)")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("           (||) ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("          (||)  ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("         (||)   ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("        (||)    ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("       (||)     ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("      (||)      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("     (||)E      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("    (||)ME      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("   (||)AME      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("  (||)GAME      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout(" (||) GAME      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("(||)  GAME      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("||)   GAME      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("|)    GAME      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout(")     GAME      ")
    utime.sleep(0.15)
    lcd.setCursor(0, 1)
    lcd.printout("      GAME      ")
    utime.sleep(2)
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.printout("     START!     ")
    utime.sleep(2)
    reset_screen()

def play_game_won_animation():
    lcd.clear()
    lcd.setRGB(0, 128, 0)
    utime.sleep(2)
    lcd.setCursor(0, 0)
    lcd.printout("CONGRATULATIONS!")
    utime.sleep(1)
    lcd.setCursor(0, 1)
    lcd.printout("    YOU WON!    ")
    utime.sleep(5)
    reset_screen()

def play_game_over_animation():
    lcd.clear()
    lcd.setRGB(128, 0, 0)
    utime.sleep(2)
    lcd.setCursor(0, 0)
    lcd.printout("YOU SUCK AT THIS")
    utime.sleep(1)
    lcd.setCursor(0, 1)
    lcd.printout("   GAME OVER!   ")
    utime.sleep(4)
    reset_screen()

def reset_screen():
    lcd.setRGB(64, 128, 64)
    lcd.clear()

def play_level_passed_animation():
    lcd.clear()
    lcd.setRGB(255, 255, 0)
    lcd.setCursor(0, 0)
    lcd.printout(f"Level {level} Passed!")
    lcd.setCursor(0, 1)
    lcd.printout(f"Next: Level {level + 1}")
    utime.sleep(2)
    reset_screen()

def play_level_lost_animation():
    lcd.clear()
    lcd.setRGB(255, 0, 0)
    lcd.setCursor(0, 0)
    lcd.printout(f"Level {level} Lost!")
    lcd.setCursor(0, 1)
    lcd.printout(f"Retrying Level {level - 1}")
    utime.sleep(2)
    reset_screen()

def reset_game():
    global car_x, car_y, car_prev_x, car_prev_y, obstacles, score, level, score_target
    car_x, car_y = 0, 0
    car_prev_x, car_prev_y = 0, 0
    obstacles = []
    score = 0
    level = 1
    score_target = 3  # Reset to initial score target
    lcd.clear()

def reset_level():
    global car_x, car_y, car_prev_x, car_prev_y, obstacles, score, score_target
    car_x, car_y = 0, 0
    car_prev_x, car_prev_y = 0, 0
    obstacles = []
    score = 0
    score_target = 2 + level  # Adjust score_target based on current level
    lcd.clear()

def play_game_race():
    global level
    play_game_intro_animation()
    reset_game()

    while True:
        move_car()
        spawn_obstacle()
        move_obstacles()
        draw_car()  # Ensure car is drawn after obstacles
        print_game_stats()

        if check_collision():
            if level == 1:
                play_game_over_animation()
                reset_game()
                break
            else:
                play_level_lost_animation()
                level -= 1
                reset_level()

        if score >= score_target:
            if level == level_target:
                play_game_won_animation()
                reset_game()
                break
            else:
                play_level_passed_animation()
                level += 1
                reset_level()

        utime.sleep(0.1)
