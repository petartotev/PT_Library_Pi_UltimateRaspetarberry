from machine import Pin
import time
import random
import RGB1602

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
#lcd = RGB1602.RGB1602(16, 2)
#lcd.setRGB(64, 128, 64)
#lcd.clear()
#lcd.setCursor(0, 0)
#lcd.setCursor(0, 1)
#lcd.printout("Your text here")

########## GPS ##########
def get_gps_coordinates():
    return generate_random_bulgaria_coordinates()

def generate_random_bulgaria_coordinates():
    """Generate random latitude and longitude within Bulgaria."""
    min_lat, max_lat = 41.2354, 44.2155  # Bulgaria's latitude range
    min_lon, max_lon = 22.357, 28.6093   # Bulgaria's longitude range
    
    latitude = round(random.uniform(min_lat, max_lat), 6)
    longitude = round(random.uniform(min_lon, max_lon), 6)
    
    return latitude, longitude

#################### MAIN PROGRAM ####################
pause_minutes_list_values = [0.25, 0.5, 1, 2, 5, 10, 15, 20, 30, 45, 60, 120, 180, 240, 360, 1440]
pause_index_curr = 0

def set_pause():
    """Allows user to set pause interval using buttons."""
    global pause_index_curr
    print("Set pause in minutes:")
    time.sleep(2)
    while True:
        if btn_green.value() == 0 or btn_red.value() == 0:
            return
        if btn_yellow.value() == 0:
            pause_index_curr = pause_index_curr + 1 if pause_index_curr + 1 < len(pause_minutes_list_values) else 0
            print(f'Current pause in minutes: {pause_minutes_list_values[pause_index_curr]}')
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        set_pause()
        print(f'Final pause in minutes: {pause_minutes_list_values[pause_index_curr]}')
        print("Program successfully started!")        
        while True:
            try:
                led.on()
                latitude, longitude = get_gps_coordinates()
                print(f'GPS {latitude}, {longitude}')
                
                total_sleep = pause_minutes_list_values[pause_index_curr] * 60
                sleep_step = 0.5
                elapsed = 0
                
                while elapsed < total_sleep:
                    if btn_red.value() == 0:
                        print("Red button pressed! Exiting...")
                        raise KeyboardInterrupt
                    time.sleep(sleep_step)
                    elapsed += sleep_step
            except KeyboardInterrupt:
                raise
            except Exception as ex:
                led.off()
                print(f"Ooops... Unexpected exception on local level! {str(ex)}")
                time.sleep(60)
    except KeyboardInterrupt:
        print("Keyboard Interrupt... Goodbye!")
    except Exception as ex:
        print(f"Ooops... Unexpected exception on general level! {str(ex)}")
        #continue # In case of unexpected exceptions here, I want to kill the program.
    finally:
        led.off()

