"""
main - Project Pico W Weather Station
"""

import RGB1602
import time
import secrets
from machine import Pin
from wifi_manager import connect_to_wifi
from ntp_manager import set_pico_rtc, get_bulgaria_time
from dust_manager import get_data_from_dust_sensor, get_air_quality_index_evaluation
from temp_manager import get_data_from_dht22_sensor
from google_manager import send_data


lcd = RGB1602.RGB1602(16, 2)
lcd.setRGB(64, 128, 64)

time_to_sleep = 5


def handle_issue(method_name, message, severity):
    severity = correct_issue_severity_if_invalid(severity)
    severity_label = get_severity_label(severity)
    bg_time = get_bulgaria_time()
    log_entry = f"{bg_time} | {severity_label.upper()}: [{method_name}] {message}\n"
    print(log_entry)
    printout_error(f'{severity_label.upper()} {method_name}'[:16], f'{message}')
    try:
        log_entry = f"{bg_time} | {severity_label.upper()}: [{method_name}] {message}\n"
        with open("errors.log", "a") as log_file:
            log_file.write(log_entry)
    except Exception as ex:
        print(f"Failed to write to log file: {ex}")


def correct_issue_severity_if_invalid(severity):
    """Accepts any severity from 1 to 5 and corrects it if wrong by setting its value as 5."""
    try:
        severity = int(severity)
        if severity < 1:
            severity = 1
        elif severity > 5:
            severity = 5
    except ValueError:
        severity = 5
    return severity


def get_severity_label(severity):
    """Return a string label based on severity level (1 to 5)."""
    severity = max(1, min(5, int(severity)))  # Ensure it's between 1 and 5
    severity_map = {
        1: "Trace",
        2: "Debug",
        3: "Information",
        4: "Warning",
        5: "Error",
    }
    return severity_map.get(severity, "Unknown")

def reset_lcd():
    """Reset LCD1602."""
    time.sleep(1)
    lcd.setRGB(64, 128, 64)
    lcd.clear()
    time.sleep(1)


def printout_welcome_animation():
    """Printout Welcome animation."""
    lcd.clear()
    reset_lcd()
    lcd.setCursor(0, 0)
    lcd.printout('   WELCOME TO   ')
    time.sleep(0.5)
    lcd.setCursor(0, 1)
    lcd.printout('WEATHER STATION!')
    time.sleep(1)
    lcd.setCursor(0, 0)
    lcd.printout('                ')
    reset_lcd()


def printout_goodbye_animation():
    """Play Goodbye animation."""
    lcd.clear()
    reset_lcd()
    lcd.setCursor(0, 0)
    lcd.printout('      EXIT      ')
    time.sleep(0.5)
    lcd.setCursor(0, 1)
    lcd.printout('WEATHER STATION!')
    time.sleep(1)
    lcd.setCursor(0, 0)
    lcd.printout('                ')
    reset_lcd()


def printout_success(line1, line2):
    """Print Success Message."""
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
    """Print Error Message."""
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
    """Connect to Wi-Fi."""
    if connect_to_wifi():
        printout_success('CONNECTED TO', secrets.SSID)
    else:
        handle_issue('set_wifi', 'Failed to connect to Wi-Fi!', 5)
        raise Exception('WIFI FAILED!')


def set_time():
    """Set RTC time."""
    if set_pico_rtc():
        printout_success('SUCCESS!', 'RTC TIME SET!')
    else:
        handle_issue('set_time', 'Failed to set RTC time!', 5)
        raise Exception('RTC NOT SET!')


def reset_time():
    """Reset RTC time."""
    try:
        if set_pico_rtc():
            printout_success('SUCCESS!', 'RTC TIME RESET!')
        else:
            handle_issue('reset_time', 'Failed to reset RTC time!', 4)
    except Exception as ex:
        handle_issue('reset_time', 'Exception while resetting RTC time!', 5)


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
    return datestr


def display_temperature_and_humidity():
    """Function displays temperature and humidity on LCD screen."""
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
            return temperature, humidity
        else:
            handle_issue('display_temperature_and_humidity', 'Failed to get valid temperature and/or humidity from DHT22 sensor!', 4)
            return None, None
    except Exception as ex:
        reset_lcd()
        handle_issue('display_temperature_and_humidity', 'Unexpected exception while displaying temperature and humidity!', 5)


def display_dust():
    """Function displays dust data on LCD screen."""
    try:
        lcd.clear()
        lcd.setRGB(128, 0, 0)
        p_m_values = []
        avg_p_m = 0
        avg_density = ''
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
        return avg_p_m, avg_density
    except Exception as ex:
        reset_lcd()
        handle_issue('display_dust', 'Unexpected exception while displaying dust!', 5)


def set_data_for_report(date_now, temp_now, hum_now, pm_now, density_now):
    """Function sets data object to be sent to Google Sheets."""
    data = {
        "date": date_now,
        "temperature": temp_now,
        "humidity": hum_now,
        "pm25": pm_now,
        "density": density_now
    }
    return data


def send_report_to_google(data):
    """Function sends data object to Google Sheets."""
    retry_attempts = 3
    retry_delay = 30.0  # Initial delay (seconds)

    for i in range(retry_attempts):
        try:
            is_success, error_msg = send_data(data)
            if not is_success:
                handle_issue('send_report_to_google', f'Attempt {i + 1}: {error_msg}', 4)
                if (i < retry_attempts - 1):
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Double the delay each retry
                continue
            return

        except Exception as ex:
            reset_lcd()
            handle_issue('send_report_to_google', f'Attempt {i + 1}: {str(ex)}!', 5)
            if (i < retry_attempts - 1):
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the delay each retry

    handle_issue('send_report_to_google', f'Failed to send data to Google Sheets after {retry_attempts} attempts!', 5)

def run_weather_station():
    """Executes the main logic of the weather station in an infinite loop."""
    time_already_reset = False
    report_already_sent = False
    while True:
        try:
            date_now = display_date_and_time()
            hour_now, minute_now = date_now[1].split(":")[:2]
            pm_now, density_now = display_dust()
            temp_now, hum_now = display_temperature_and_humidity()
            if (hour_now == '23' and minute_now == '59'):
                if not time_already_reset:
                    time_already_reset = True
                    reset_time()
            else:
                time_already_reset = False
            if minute_now == '00' or minute_now == '30':
                if not report_already_sent:
                    send_report_to_google(set_data_for_report(' '.join(date_now), temp_now, hum_now, pm_now, density_now))
                    report_already_sent = True
            else:
                report_already_sent = False
        except KeyboardInterrupt:
            handle_issue('run_weather_station', 'KeyboardInterrupt', 5)
            raise
        except Exception as ex:
            handle_issue('run_weather_station', str(ex), 5)


if __name__ == "__main__":
    try:
        printout_welcome_animation()
        set_wifi()
        set_time()
        run_weather_station()
    except KeyboardInterrupt:
        handle_issue('__main__', 'KeyboardInterrupt', 5)
    except Exception as ex:
        handle_issue('__main__', str(ex), 5)
    finally:
        printout_goodbye_animation()
