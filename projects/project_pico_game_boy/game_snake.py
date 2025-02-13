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
snake = [(6, 0)]  # Initial snake position
snake_dir = (1, 0)  # Moving right initially
food = (random.randint(0, 13), random.randint(0, 1))

score = 0
score_target = 1
level = 1
level_target = 3


def move_snake():
    global snake, snake_dir, food, score
    head_x, head_y = snake[0]
    new_head = (head_x + snake_dir[0], head_y + snake_dir[1])

    # Check for wall collisions
    if new_head[0] < 0 or new_head[0] > 13 or new_head[1] < 0 or new_head[1] > 1:
        return False

    # Check for self-collision
    if new_head in snake:
        return False

    snake.insert(0, new_head)

    # Check for food collision
    if new_head == food:
        score += 1
        spawn_food()
    else:
        snake.pop()

    return True


def spawn_food():
    global food
    while True:
        new_food = (random.randint(0, 13), random.randint(0, 1))
        if new_food not in snake:
            food = new_food
            break


def change_direction():
    global snake_dir
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    if yValue <= 600 and snake_dir != (0, 1):  # up
        snake_dir = (0, -1)
    elif yValue >= 60000 and snake_dir != (0, -1):  # down
        snake_dir = (0, 1)
    elif xValue <= 600 and snake_dir != (1, 0):  # left
        snake_dir = (-1, 0)
    elif xValue >= 60000 and snake_dir != (-1, 0):  # right
        snake_dir = (1, 0)


def draw_game():
    lcd.clear()
    for segment in snake:
        lcd.setCursor(segment[0], segment[1])
        lcd.printout("#")
    lcd.setCursor(food[0], food[1])
    lcd.printout("*")
    lcd.setCursor(14, 0)
    lcd.printout(f"L{level}")
    lcd.setCursor(14, 1)
    lcd.printout(f"{score:02}")


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
    global level
    lcd.clear()
    lcd.setRGB(128, 0, 0)
    utime.sleep(1)
    lcd.setCursor(0, 0)
    lcd.printout(f"   YOU FAILED   ")
    utime.sleep(2)
    lcd.setCursor(0, 1)
    lcd.printout(f"    LEVEL {(level):02}    ")
    utime.sleep(3)
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
    reset_game()
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
    reset_game()
    reset_screen()


def reset_screen():
    lcd.setRGB(64, 128, 64)
    lcd.clear()
    lcd.setCursor(0, 0)


def reset_game():
    global snake, snake_dir, food, score, level, score_target
    snake = [(6, 0)]
    snake_dir = (1, 0)
    food = (random.randint(0, 13), random.randint(0, 1))
    score = 0
    level = 1
    score_target = 1
    lcd.clear()


def reset_level():
    global snake, snake_dir, food, score, score_target
    snake = [(6, 0)]
    snake_dir = (1, 0)
    food = (random.randint(0, 13), random.randint(0, 1))
    score = 0
    score_target = 1 + (level - 1)
    lcd.clear()


def play_game_snake():
    global level
    reset_game()

    while True:
        change_direction()
        if not move_snake():
            if level == 1:
                play_game_over_animation()
                break
            else:
                level -= 1
                play_level_lost_animation()
                reset_level()

        if score >= score_target:
            if level == level_target:
                play_game_won_animation()
                break
            else:
                play_level_passed_animation()
                level += 1
                reset_level()

        draw_game()
        utime.sleep(0.7)
