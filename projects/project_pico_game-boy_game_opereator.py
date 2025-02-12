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
player_x = 0
player_y = 0
player_x_prev = 0
player_y_prev = 0

reward_active = False
reward_x = -1
reward_y = -1
reward_type = '+'  # Can be '+' or '-'
reward_timer = 0

score = 0
score_target = 3
score_target_default = 3
level = 1
level_target = 3

##### Player #####
def set_player_position_by_joystick_input():
    global player_x, player_y, player_x_prev, player_y_prev
    xValue = xAxis.read_u16()
    yValue = yAxis.read_u16()
    buttonValue = button.value()
    player_x_prev = player_x
    player_y_prev = player_y
    if xValue <= 600: # left
        player_x = player_x - 1 if player_x > 0 else 13
    elif xValue >= 60000: # right
        player_x = player_x + 1 if player_x < 13 else 0
    if yValue <= 600: # up
        player_y = 0
    elif yValue >= 60000: # down
        player_y = 1
    if buttonValue == 0: # pressed
        print("pressed!")

def print_player(pl_x, pl_y):
    global player_x_prev, player_y_prev
    lcd.setCursor(pl_x, pl_y)
    #print(f"x: {pl_x}, y: {pl_y}")
    lcd.printout("O")
    if (player_x_prev != pl_x or player_y_prev != pl_y):
        lcd.setCursor(player_x_prev, player_y_prev)
        lcd.printout(" ")

def move_player():
    set_player_position_by_joystick_input()
    print_player(player_x, player_y)
    utime.sleep(0.1)
    
def reset_player():
    global player_x, player_y, player_x_prev, player_y_prev
    player_x = 0
    player_y = 0
    player_x_prev = 0
    player_y_prev = 0

def reset_game():
    global score, score_target, level, level_target
    score = 0
    score_target = score_target_default
    level = 1

##### Reward #####
def spawn_reward():
    global reward_active, reward_x, reward_y, reward_type, reward_timer
    if not reward_active and random.random() < 0.05:  # 5% chance to spawn
        reward_x, reward_y = random.randint(0, 13), random.randint(0, 1)
        while reward_x == player_x and reward_y == player_y:
            reward_x, reward_y = random.randint(0, 13), random.randint(0, 1)
        reward_type = random.choice(['+', '-'])
        reward_timer = max(20 - level * 2, 5)  # Timer decreases with level
        reward_active = True
        lcd.setCursor(reward_x, reward_y)
        lcd.printout(reward_type)

def update_reward():
    global reward_active, reward_timer, score
    if reward_active:
        if player_x == reward_x and player_y == reward_y:
            score = score + 1 if reward_type == '+' else -1
            clear_reward()
        else:
            reward_timer -= 1
            if reward_timer <= 0:
                clear_reward()

def clear_reward():
    global reward_active
    lcd.setCursor(reward_x, reward_y)
    lcd.printout(" ")
    reward_active = False

##### Animations #####
def play_game_intro_animation():
    lcd.clear()
    lcd.setRGB(0, 0, 255)
    utime.sleep(1)
    lcd.setRGB(0, 255, 0)
    utime.sleep(0.75)
    lcd.setRGB(255, 0, 0)
    utime.sleep(0.5)
    lcd.setCursor(0, 0)
    lcd.printout("   OPEREATOR!   ")
    utime.sleep(0.5)
    lcd.setCursor(0, 1)
    lcd.printout(" +    GAME    - ")
    utime.sleep(1)
    lcd.setCursor(0, 1)
    lcd.printout("                ")
    utime.sleep(0.5)
    lcd.setCursor(0, 0)
    lcd.printout("                ")
    utime.sleep(0.5)
    lcd.setRGB(0, 255, 0)
    utime.sleep(0.75)
    reset_screen()
    utime.sleep(1)

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

def play_level_won_animation():
    global level
    lcd.clear()
    lcd.setRGB(0, 96, 0)
    utime.sleep(1)
    lcd.setCursor(0, 0)
    lcd.printout(f"LEVEL {level:02} PASSED!")
    utime.sleep(1)
    lcd.setCursor(0, 1)
    next_level_str = f"    LEVEL {(level + 1):02}    " if level + 1 < level_target else "  FINAL LEVEL!  "
    lcd.printout(next_level_str)
    utime.sleep(3)
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
    lcd.printout(f"    LEVEL {(level - 1):02}    ")
    utime.sleep(3)
    reset_screen()

def reset_screen():
    lcd.setRGB(64, 128, 64)
    lcd.clear()

##### Game Helpers #####
def is_game_complete():
    return level == level_target and is_level_complete()

def is_level_complete():
    return score >= score_target

def check_if_dead():
    global score, level, score_target
    is_game_finalized = False
    if score < 0:
        if level <= 1:
            play_game_over_animation()
            reset_game()
            is_game_finalized = True
        else:
            play_level_lost_animation()
            score_target -= 1
        score = 0
        level = 1 if level <= 1 else level - 1
        reset_player()
        return is_game_finalized

def check_if_won():
    global level, score, score_target
    is_game_finalized = False
    if is_level_complete():
        if is_game_complete():
            play_game_won_animation()
            reset_game()
            is_game_finalized = True
        else:
            play_level_won_animation()
            level += 1
            score = 0
            score_target += 1
        reset_player()
        return is_game_finalized

def print_game_stats():
    lcd.setCursor(14, 0)
    lcd.printout(f"L{level}")
    lcd.setCursor(14, 1)
    lcd.printout(f"{score:02}")

##### GAME #####
def play_game_opereator():
    try:
        play_game_intro_animation()
        while True:
            move_player()
            spawn_reward()
            update_reward()
            print_game_stats()
            if check_if_dead():
                break
            if (check_if_won()):
                break
    except Exception as ex:
        print(ex)
        reset_game()
        reset_player()
