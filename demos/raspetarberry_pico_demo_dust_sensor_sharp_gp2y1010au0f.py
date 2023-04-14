"""Raspetarberry Pi project to consume DHT22 sensor data and display it on LCD screen."""

import time
from machine import Pin,ADC
import utime

# Sharp GP2Y1010AU0F Dust Sensor

#Select ADC input 0 (GPIO26)
COV_RATIO     =  0.2 #ug/mmm / mv
NO_DUST_VOLTAGE = 400  #mv
SYS_VOLTAGE = 3300

class Dust:
    def __init__(self):
         #Select ADC input 0 (GPIO26)
        self.ADC_ConvertedValue = machine.ADC(0)
        self.DIN = Pin(22,Pin.OUT)
        self.conversion_factor = 3.3 / (65535)
        self.flag_first = 0
        self.buff = [0,0,0,0,0,0,0,0,0,0]
        self.sum1 = 0
    def Filter(self,ad_value):      
        buff_max = 10
        if self.flag_first == 0:
            self.flag_first = 1
            for i in range (buff_max):
                self.buff[i] = ad_value
                self.sum1 = self.sum1+self.buff[i]
            return ad_value
        else:
            self.sum1 = self.sum1-self.buff[0]
            for i in range (buff_max-1):
                self.buff[i] = self.buff[i+1]
            self.buff[9] = ad_value
            self.sum1 = self.sum1 + self.buff[9]
            i = self.sum1 / 10.0
            return i

def get_air_quality_particulate_matter():
    """Function gets particulate matter PM2.5 density value from dust sensor."""
    Dust.DIN.value(1 )
    utime.sleep_us(280)
    AD_value = Dust.ADC_ConvertedValue.read_u16()
    Dust.DIN.value(0)
    AD_value = Dust.Filter(AD_value)
    voltage = (SYS_VOLTAGE / 65536.0) * AD_value * 11
    if voltage >= NO_DUST_VOLTAGE:
        voltage = voltage - NO_DUST_VOLTAGE
        density = voltage * COV_RATIO
    else:
        density = 0     
    utime.sleep(1)
    return density

def get_air_quality_index_evaluation(density):
    """Function returns EPA AQI evaluation based on PM2.5 density."""
    if density is None:
        return "Unknown"
    density = int(density)
    if 0 <= density <= 12.0:
        return "Good"
    if 12.1 <= density <= 35.4:
        return "Moderate"
    if 35.5 <= density <= 55.4:
        return "Unhealthy for Sensitive Groups"
    if 55.5 <= density <= 150.4:
        return "Unhealthy"
    if 150.5 <= density < 250.4:
        return "Very Unhealthy"
    if 250.5 <= density <= 500:
        return "Hazardous"
    return "Unknown"

def print_data_from_dust_sensor():
    """Function prints data gathered from sensors."""
    p_m = round(get_air_quality_particulate_matter(), 1)
    evaluation = get_air_quality_index_evaluation(p_m)
    date_now = utime.localtime()
    if date_now[4] in (0,5,10,15,20,25,30,35,40,45,50,55):
        date_str = f'{date_now[0]}-{'{:02d}'.format(date_now[1])}-{'{:02d}'.format(date_now[2])}'
        time_str = f'{'{:02d}'.format(date_now[3])}:{'{:02d}'.format(date_now[4])}:{'{:02d}'.format(date_now[5])}'
        print(f'{date_str} {time_str},{p_m},{evaluation}')
        time.sleep(60)

def welcome():
    """Function prints welcome."""
    print("Welcome!")
    time.sleep(3)

def play():
    """Function plays the program loop."""
    welcome()
    while True:
        try:
            print_data_from_dust_sensor()
        except RuntimeError as error:
            # Errors occur often with DHT sensors as they are hard to read, so just keep going.
            print("Runtime error!")
            print(error.args[0])
            continue
        except Exception as error:
            print("Exception error!")
            raise error
        finally:
            time.sleep(0.5)

def close():
    """Function prints goodbye."""
    print("Bye!")
    time.sleep(3)

if __name__ == "__main__":
    try:
        Dust=Dust()
        play()
    except KeyboardInterrupt:
        close()
    finally:
        print("Exit!")
