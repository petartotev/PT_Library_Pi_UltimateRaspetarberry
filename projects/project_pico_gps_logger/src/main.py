from machine import Pin
import time
import random
import RGB1602
from gps_manager import get_gps_location
########## LED ##########
led = Pin(25, Pin.OUT)
# led.on()
# led.off()
# led.toggle()

########## BUTTONS ##########
btn_green = Pin(18, Pin.IN, Pin.PULL_UP)
btn_yellow = Pin(17, Pin.IN, Pin.PULL_UP)
btn_red = Pin(16, Pin.IN, Pin.PULL_UP)

########## LCD RGB 1602 ##########
lcd = RGB1602.RGB1602(16, 2)
lcd.setRGB(64, 128, 64)
#lcd.clear()
#lcd.setCursor(0, 0)
#lcd.setCursor(0, 1)
#lcd.printout("Your text here")

def display_message(line_1, line_2, log_level = 0):
    lcd.clear()
    lcd.setCursor(0, 0)
    set_lcd_color_by_log_level(log_level)
    lcd.printout(line_1)
    if line_2 != "":
        lcd.setCursor(0, 1)
        lcd.printout(line_2)
    time.sleep(2)
    lcd.setRGB(64, 128, 64)

def lcd_clear_second_line():
    lcd.setCursor(0, 1)
    lcd.printout("                ")

def set_lcd_color_by_log_level(log_level):
    if log_level == 5: # error
        lcd.setRGB(255, 0, 0)
    elif log_level == 3: # info (success)
        lcd.setRGB(0, 255, 0)
    else:
        lcd.setRGB(64, 128, 64)

########## GPS ##########
def get_mocked_gps_coordinates():
    return generate_random_bulgaria_coordinates()

def generate_random_bulgaria_coordinates():
    """Generate random latitude and longitude within Bulgaria."""
    min_lat, max_lat = 41.2354, 44.2155  # Bulgaria's latitude range
    min_lon, max_lon = 22.357, 28.6093   # Bulgaria's longitude range
    
    latitude = round(random.uniform(min_lat, max_lat), 6)
    longitude = round(random.uniform(min_lon, max_lon), 6)
    
    return latitude, longitude

def log_gps_coordinates(latitude, longitude, altitude):
    try:
        log_entry = f"{get_formatted_date()},{latitude},{longitude},{altitude}\n"
        with open("gps_coords.log", "a") as log_file:
            log_file.write(log_entry)
    except Exception as ex:
        display_message("Failed to log!", "", 5)

def get_formatted_date():
    time_now = time.localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(time_now[0], time_now[1], time_now[2], time_now[3], time_now[4], time_now[5])

#################### MAIN PROGRAM ####################
pause_minutes_list_values = [0, 0.02, 0.05, 0.10, 0.25, 0.5, 1, 2, 5, 10, 15, 20, 30, 45, 60, 120, 180, 240, 360, 1440]
pause_index_curr = 0

def set_pause():
    """Allows user to set pause interval using buttons."""
    global pause_index_curr
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout("Set pause:")
    time.sleep(0.5)
    while True:
        lcd.setCursor(0, 1)
        lcd.printout(str(pause_minutes_list_values[pause_index_curr]))
        if btn_green.value() == 0 or btn_red.value() == 0:
            break
        if btn_yellow.value() == 0:
            pause_index_curr = pause_index_curr + 1 if pause_index_curr + 1 < len(pause_minutes_list_values) else 0
            time.sleep(0.2)
            lcd_clear_second_line()
    display_message("Pause set!", "", 3)

def set_pico_time():
    years = [2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034, 2035]
    years_index_curr = 0
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    months_index_curr = 0
    days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    days_index_curr = 0
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days_of_week_index_curr = 0
    hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    hours_index_curr = 0
    minutes = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    minutes_index_curr = 0

    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout("Set year:")
    time.sleep(0.5)
    while True:
        lcd.setCursor(0, 1)
        lcd.printout(str(years[years_index_curr]))
        if btn_green.value() == 0 or btn_red.value() == 0:
            break
        if btn_yellow.value() == 0:
            years_index_curr = years_index_curr + 1 if years_index_curr + 1 < len(years) else 0
            time.sleep(0.2)
            lcd_clear_second_line()

    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout("Set month:")
    time.sleep(0.5)
    while True:
        lcd.setCursor(0, 1)
        lcd.printout(str(months[months_index_curr]))
        if btn_green.value() == 0 or btn_red.value() == 0:
            break
        if btn_yellow.value() == 0:
            months_index_curr = months_index_curr + 1 if months_index_curr + 1 < len(months) else 0
            time.sleep(0.2)
            lcd_clear_second_line()

    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout("Set day:")
    time.sleep(0.5)
    while True:
        lcd.setCursor(0, 1)
        lcd.printout(str(days[days_index_curr]))
        if btn_green.value() == 0 or btn_red.value() == 0:
            break
        if btn_yellow.value() == 0:
            days_index_curr = days_index_curr + 1 if days_index_curr + 1 < len(days) else 0
            time.sleep(0.2)
            lcd_clear_second_line()

    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout("Set day of week:")
    time.sleep(0.5)
    while True:
        lcd.setCursor(0, 1)
        lcd.printout(str(days_of_week[days_of_week_index_curr]))
        if btn_green.value() == 0 or btn_red.value() == 0:
            break
        if btn_yellow.value() == 0:
            days_of_week_index_curr = days_of_week_index_curr + 1 if days_of_week_index_curr + 1 < len(days_of_week) else 0
            time.sleep(0.2)
            lcd_clear_second_line()

    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout("Set hour:")
    time.sleep(0.5)
    while True:
        lcd.setCursor(0, 1)
        lcd.printout(str(hours[hours_index_curr]))
        if btn_green.value() == 0 or btn_red.value() == 0:
            break
        if btn_yellow.value() == 0:
            hours_index_curr = hours_index_curr + 1 if hours_index_curr + 1 < len(hours) else 0
            time.sleep(0.2)
            lcd_clear_second_line()

    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout("Set minute:")
    time.sleep(0.5)
    while True:
        lcd.setCursor(0, 1)
        lcd.printout(str(minutes[minutes_index_curr]))
        if btn_green.value() == 0 or btn_red.value() == 0:
            break
        if btn_yellow.value() == 0:
            minutes_index_curr = minutes_index_curr + 1 if minutes_index_curr + 1 < len(minutes) else 0
            time.sleep(0.2)
            lcd_clear_second_line()

    rtc = machine.RTC()
    rtc.datetime(
        (
            years[years_index_curr], # year
            months[months_index_curr], # month
            days[days_index_curr], # day
            days_of_week_index_curr, # weekday (0 = Monday, 6 = Sunday)
            hours[hours_index_curr], # hour
            minutes[minutes_index_curr], # minute
            0, # second
            0, # subseconds (not used)
        )
    )
    display_message("Time set!", "", 3)

if __name__ == "__main__":
    try:
        set_pause()
        set_pico_time()
        display_message("Program started!", "", 3)
        while True:
            try:
                led.on()
                latitude, longitude, altitude = get_gps_location()
                display_message(f"{latitude[:10]}", f"{longitude[:10]} {int(altitude):04d}m")
                log_gps_coordinates(latitude, longitude, altitude)
                total_sleep = pause_minutes_list_values[pause_index_curr] * 60
                sleep_step = 0.5
                elapsed = 0
                
                while elapsed < total_sleep:
                    if btn_red.value() == 0:
                        display_message("Red button pressed!", "Exiting...", 5)
                        raise KeyboardInterrupt
                    time.sleep(sleep_step)
                    elapsed += sleep_step
            except KeyboardInterrupt:
                raise
            except Exception as ex:
                led.off()
                lcd.clear()
                display_message("Local error!", f"{str(ex)}", 5)
                time.sleep(60)
    except KeyboardInterrupt:
        display_message("Keyboard Interrupt...", "Goodbye!", 5)
    except Exception as ex:
        display_message("Global error!", f"{str(ex)}", 5)
        #continue # In case of unexpected exceptions here, I want to kill the program.
    finally:
        led.off()
        lcd.clear()
