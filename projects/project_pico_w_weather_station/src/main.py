import RGB1602
import time
import secrets
from machine import Pin
from wifi_manager import connect_to_wifi
from ntp_manager import set_pico_rtc, get_bulgaria_time
from dust_manager import get_data_from_dust_sensor, get_air_quality_index_evaluation
from temp_manager import get_data_from_dht22_sensor

lcd = RGB1602.RGB1602(16, 2)
lcd.setRGB(64, 128, 64)

time_to_sleep = 5

########## LCD ##########

def reset_lcd():
    """Reset LCD1602"""
    global lcd
    time.sleep(1)
    lcd.setRGB(64, 128, 64)
    lcd.clear()
    time.sleep(1)

def printout_welcome_animation():
    """Printout Welcome animation"""
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout('   WELCOME TO   ')
    time.sleep(1)
    lcd.setCursor(0, 1)
    lcd.printout('WEATHER STATION!')
    time.sleep(1)
    lcd.setCursor(0, 0)
    lcd.printout('                ')
    reset_lcd()

def printout_goodbye_animation():
    """Play Goodbye animation"""
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.printout('      EXIT      ')
    time.sleep(1)
    lcd.setCursor(0, 1)
    lcd.printout('WEATHER STATION!')
    time.sleep(1)
    lcd.setCursor(0, 0)
    lcd.printout('                ')
    reset_lcd()

def printout_success(line1, line2):
    lcd.clear()
    time.sleep(1)
    lcd.setRGB(0, 128, 0)
    lcd.setCursor(0, 0)
    lcd.printout(f'{line1[:16]}')
    time.sleep(1)
    lcd.setCursor(0, 1)
    lcd.printout(f'{line2[:16]}')
    reset_lcd()

def printout_error(line1, line2):
    lcd.clear()
    time.sleep(1)
    lcd.setRGB(128, 0, 0)
    lcd.setCursor(0, 0)
    lcd.printout(f'{line1[:16]}')
    time.sleep(1)
    lcd.setCursor(0, 1)
    lcd.printout(f'{line2[:16]}')
    reset_lcd()

def set_wifi():
    if connect_to_wifi():
        printout_success('CONNECTED TO', secrets.SSID)
    else:
        print('set_wifi() failed!')
        raise Exception('WIFI FAILED!')

def set_time():
    if set_pico_rtc():
        printout_success('SUCCESS!', 'RTC TIME SET!')
    else:
        print('set_pico_rtc() failed!!!')
        raise Exception('RTC NOT SET!')
    
def reset_time():
    try:
        if set_pico_rtc():
            printout_success('SUCCESS!', 'RTC TIME RESET!')
        else:
            print('set_pico_rtc() failed!!!')
    except Exception as ex:
        print(f'Error: {ex}')

def display_date_and_time():
    """Function displays date and time on LCD screen."""
    global time_to_sleep
    datestr = ''
    for _ in range(time_to_sleep):
        datestr = get_bulgaria_time().split()
        lcd.setRGB(64, 128, 64)
        lcd.setCursor(0, 0)
        lcd.printout(datestr[0][:16])
        lcd.setCursor(0, 1)
        lcd.printout(datestr[1][:16])
        time.sleep(1)
    return datestr[1].split(":")[:2]

def display_temperature_and_humidity():
    try:
        temperature, humidity = get_data_from_dht22_sensor()
        if temperature is not None and humidity is not None:
            lcd.setRGB(227, 214, 12)
            lcd.setCursor(0, 0)
            lcd.printout(f"Temp: {temperature:.1f}'C")
            lcd.setCursor(0, 1)
            lcd.printout(f"Humidity: {humidity:.1f}%")
            time.sleep(time_to_sleep)
            lcd.clear()
        else:
            print("Failed to get temperature/humidity data.")
    except Exception as ex:
        reset_lcd()
        print(f"ERROR: DHT22 failed! {ex}")

def display_dust():
    try:
        lcd.clear()
        lcd.setRGB(128, 0, 0)
        p_m_values = []
        for i in range(time_to_sleep):
            p_m, _ = get_data_from_dust_sensor()
            p_m_values.append(p_m)
            avg_p_m = sum(p_m_values) / len(p_m_values)
            avg_density = get_air_quality_index_evaluation(avg_p_m)
            lcd.setCursor(0, 0)
            lcd.printout(f'{avg_p_m:.1f} mg/m3             '[:16])
            lcd.setCursor(0, 1)
            lcd.printout(f'{avg_density}             '[:16])
            time.sleep(1)
        lcd.clear()
    except Exception as ex:
        reset_lcd()
        print(f"ERROR: Dust failed! {ex}")

def execute_weather_station_flow():
    is_time_already_reset_today = False
    while True:
        hour_now, minute_now = display_date_and_time()
        display_dust()
        display_temperature_and_humidity()
        if (hour_now == '23' and minute_now == '59'):
            if not already_reset_today:
                already_reset_today = True
                reset_time()
        else:
            already_reset_today = False

if __name__ == "__main__":
    try:
        reset_lcd()
        printout_welcome_animation()
        set_wifi()
        set_time()
        execute_weather_station_flow()
    except KeyboardInterrupt:
        printout_error('ERROR', 'KeyboardInterrupt...')
    except Exception as ex:
        print(f'Error: {ex}')
        printout_error('ERROR', str(ex))
    finally:
        lcd.clear()
        printout_goodbye_animation()
