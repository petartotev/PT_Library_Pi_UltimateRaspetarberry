from machine import Pin, ADC
import RGB1602
import utime
from game_opereator import play_game_opereator
from game_race import play_game_race
from game_snake import play_game_snake

# LCD
lcd = RGB1602.RGB1602(16, 2)
lcd.setRGB(64, 128, 64)

# Joystick
xAxis = ADC(Pin(27))
yAxis = ADC(Pin(26))
button = Pin(16, Pin.IN, Pin.PULL_UP)

# Games List
games_list = ['OperEator', 'Race', 'Snake']
game_chosen = 0

def play_main_intro_animation():
    lcd.clear()
    lcd.setRGB(0, 0, 255)
    utime.sleep(1)
    lcd.setRGB(0, 255, 0)
    utime.sleep(0.75)
    lcd.setRGB(255, 0, 0)
    utime.sleep(0.5)
    lcd.setCursor(0, 0)
    lcd.printout("      GAME      ")
    utime.sleep(0.5)
    lcd.setCursor(0, 1)
    lcd.printout("    CONSOLE!    ")
    utime.sleep(1)
    lcd.setCursor(0, 1)
    lcd.printout("                ")
    utime.sleep(0.5)
    lcd.setCursor(0, 0)
    lcd.printout("                ")
    utime.sleep(0.5)
    lcd.setRGB(0, 255, 0)
    utime.sleep(0.75)
    lcd.setRGB(64, 128, 64)
    lcd.clear()
    utime.sleep(1)

def play_missing_game_animation():
    global level
    lcd.clear()
    lcd.setRGB(128, 0, 0)
    utime.sleep(1)
    lcd.setCursor(0, 0)
    lcd.printout(f"GAME IS MISSING!")
    utime.sleep(1)
    lcd.setCursor(0, 1)
    lcd.printout(f" CHOOSE ANOTHER ")
    utime.sleep(2)
    lcd.setRGB(64, 128, 64)
    lcd.clear()

def choose_game():
    global game_chosen, games_list
    while True:
        xValue = xAxis.read_u16()
        yValue = yAxis.read_u16()
        buttonValue = button.value()
        lcd.setCursor(2, 0)
        lcd.printout(games_list[game_chosen])
        lcd.setCursor(0, 1)
        if (game_chosen == 0):
            lcd.printout("               >")
        elif (game_chosen == len(games_list) - 1):
            lcd.printout("<               ")
        else:
            lcd.printout("<              >")
        if xValue <= 600: # left
            if game_chosen > 0:
                lcd.setCursor(0, 0)
                lcd.printout("                ")
            game_chosen = game_chosen - 1 if game_chosen > 0 else 0
            utime.sleep(0.4)
        elif xValue >= 60000: # right
            if game_chosen < len(games_list) - 1:
                lcd.setCursor(0, 0)
                lcd.printout("                ")
            game_chosen = game_chosen + 1 if game_chosen < len(games_list) - 1 else len(games_list) - 1
            utime.sleep(0.4)
        if buttonValue == 0: # pressed
            print("pressed!")
            play_game_by_index()

def play_game_by_index():
    global game_chosen
    if game_chosen == 0: # OperEator
        play_game_opereator()
    elif game_chosen == 1: # Race
        play_game_race()
    elif game_chosen == 2: # Snake
        play_game_snake()
    else:
        play_missing_game_animation()

def print_error(ex):
    utime.sleep(1)
    lcd.setRGB(128, 0, 0)
    lcd.setCursor(0, 0)
    lcd.printout(ex[:16])
    print(f"Error! {ex}")
    utime.sleep(5)
    lcd.setRGB(64, 128, 64)
    lcd.clear()

if __name__ == "__main__":
    play_main_intro_animation()
    try:
        choose_game()
    except KeyboardInterrupt:
        print("Exit...")
    except Exception as ex:
        print_error(ex)
    finally:
        lcd.setRGB(0, 0, 0)
        lcd.clear()